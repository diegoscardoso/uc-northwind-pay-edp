SHELL := /bin/sh

PYTHON ?= python3
RUNNER_VENV := legacy/runner/.venv
RUNNER_PYTHON := $(RUNNER_VENV)/bin/python
SCENARIO ?= valid-minimal
TYPE ?= 01
OUTPUT ?= gen/output
EVIDENCE ?= evidence
POLL_INTERVAL ?= 5
MAX_BATCHES ?= 100
SUPPORTED_TYPES := 01 02 03 04 05
WORKER_E2E_SUITE := tests/end-to-end/run_worker_suite.py

# Modern: an independent second implementation with its own environment.
MODERN_VENV := modern/.venv
MODERN_PYTHON := $(MODERN_VENV)/bin/python
MODERN_SRC := modern/ingestion/src
MODERN_DUCKDB := modern/lakehouse/ducklake/northwind_modern.duckdb

# Dark Factory: additive, read-only, and never part of a legacy gate.
DF_SRC := factory/src
DF_SUITE := factory/tests/end-to-end/run_detector_suite.py
DF_EVIDENCE ?= evidence/factory
# The synchronous typed suites keep isolated evidence roots, one per type.
DF_DEFAULT_ROOTS := .runtime/e2e-evidence,.runtime/e2e-type02-evidence,.runtime/e2e-type03-evidence,.runtime/e2e-type04-evidence,.runtime/e2e-type05-evidence

.DEFAULT_GOAL := help

.PHONY: help init deploy migrate status down gen test-contracts test-gen test-python test-postgres test-java check \
	publish publish-raw run run-type run-file worker worker-once test-type01 test-e2e test-worker-e2e test clean clean-runtime \
	df-manifest df-check df-detect df-accept retool \
	modern-init modern-check modern-run modern-dbt modern-rebuild modern-dagster modern-api

help: ## List supported targets, compatibility aliases, and input variables.
	@awk 'BEGIN { \
		FS = ":.*## "; \
		print "Usage: make <target> [VARIABLE=value]"; \
		print ""; \
		print "Targets:"; \
	} \
	/^[a-zA-Z0-9_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2} \
	END { \
		print ""; \
		print "Inputs:"; \
		print "  TYPE=01|02|03|04|05|all  Type selector; run/gen/test-e2e accept all."; \
		print "  SCENARIO=name       Canonical scenario (default: valid-minimal)."; \
		print "  OUTPUT=path         DataGen output root (default: gen/output)."; \
		print "  EVIDENCE=path       Worker evidence root (default: evidence)."; \
		print "  POLL_INTERVAL=secs  Worker poll interval, 0.1 through 3600 (default: 5)."; \
		print "  MAX_BATCHES=count   Worker per-cycle bound, 1 through 100 (default: 100)."; \
		print "  BATCH=id            Bundle directory name below OUTPUT for publish."; \
		print "  BUNDLE=path         Explicit bundle directory for publish."; \
		print "  FILE=path           Raw file with sibling checksum and manifest; TYPE cannot be all."; \
		print "  CONFIRM=clean-runtime  Required destructive-clean confirmation."; \
		print ""; \
		print "BATCH and BUNDLE are mutually exclusive."; \
	}' $(MAKEFILE_LIST)

init: ## Create local Python environments, .env, and container builds.
	@test -f .env || cp .env.example .env
	@chmod 0600 .env
	@$(PYTHON) -m venv $(RUNNER_VENV)
	@$(RUNNER_PYTHON) -m pip install --quiet --upgrade pip
	@$(RUNNER_PYTHON) -m pip install --quiet -e 'gen[dev]' -r legacy/runner/requirements.txt
	@docker compose build sftp processor
	@echo "local development environment initialized"

deploy: ## Start services, migrate PostgreSQL, and verify runtime health.
	@docker compose up -d --build --wait sftp postgres
	@$(RUNNER_PYTHON) legacy/runner/bootstrap_runtime.py
	@$(MAKE) --no-print-directory migrate
	@$(RUNNER_PYTHON) legacy/runner/runtime_status.py

migrate: ## Apply immutable PostgreSQL migrations or verify checksums.
	@PYTHONPATH=legacy/runner $(RUNNER_PYTHON) legacy/postgres/migrate.py

status: ## Show Compose state and verify every local connection.
	@docker compose ps
	@$(RUNNER_PYTHON) legacy/runner/runtime_status.py

down: ## Stop services without deleting volumes or evidence.
	@docker compose down

gen: ## Generate one type, or the same scenario for all five types.
	@case "$(TYPE)" in 01|02|03|04|05|all) ;; \
		*) echo "TYPE must be one of 01, 02, 03, 04, 05, or all" >&2; exit 2 ;; \
	esac
	@if [ "$(TYPE)" = "all" ]; then \
		for type_number in $(SUPPORTED_TYPES); do \
			$(RUNNER_PYTHON) gen/src/cli.py \
				--type "$$type_number" \
				--scenario "$(SCENARIO)" \
				--output "$(OUTPUT)" \
				--contracts-root contracts/types || exit $$?; \
		done; \
	else \
		$(RUNNER_PYTHON) gen/src/cli.py \
			--type "$(TYPE)" \
			--scenario "$(SCENARIO)" \
			--output "$(OUTPUT)" \
			--contracts-root contracts/types; \
	fi

test-gen: ## Run all Python DataGen unit, contract, integration, and security tests.
	@PYTHONPATH=gen/src $(RUNNER_PYTHON) -m unittest discover \
		--start-directory gen/tests \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=gen/src $(RUNNER_PYTHON) -m mypy \
		--python-version 3.12 \
		--strict \
		gen/src

test-contracts: ## Validate executable cross-type schemas and canonical contract oracles.
	@PYTHONPATH=gen/src $(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/contracts \
		--pattern 'test_*.py' \
		--verbose

test-python: ## Run Python unit/security/oracle tests and strict worker-boundary typing.
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/intake:legacy/postgres:validation/oracle \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/unit \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/intake:legacy/postgres:validation/oracle \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/security \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/intake:legacy/postgres:validation/oracle \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory validation/oracle/tests \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/intake:legacy/postgres:validation/oracle \
		$(RUNNER_PYTHON) -m mypy \
		--python-version 3.12 \
		--strict \
		--no-incremental \
		legacy/runner/worker.py \
		legacy/runner/recovery_journal.py \
		legacy/runner/lifecycle.py \
		legacy/runner/workflow.py \
		legacy/intake/raw_intake.py \
		legacy/publisher/raw_publisher.py

test-postgres: ## Run rollback-only COPY, procedure, and permission tests.
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/postgres \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/postgres \
		--pattern 'test_*.py' \
		--verbose

test-java: ## Build Java 21 and run its parser/privacy regression suite.
	@docker compose build processor

check: test-contracts test-gen test-python test-java ## Run pure source/schema suites and build the Java image.
	@docker compose config --quiet
	@$(RUNNER_PYTHON) -m compileall -q gen/src legacy validation tests
	@$(RUNNER_PYTHON) -m json.tool contracts/common/source-manifest.schema.json >/dev/null
	@$(RUNNER_PYTHON) -m json.tool contracts/common/generation-receipt.schema.json >/dev/null
	@$(RUNNER_PYTHON) -m json.tool contracts/common/sanitized-manifest.schema.json >/dev/null

test-type01: ## Run the complete Type 01 proof on a fresh deployed runtime.
	@PYTHONPATH=gen/src $(RUNNER_PYTHON) -m unittest discover \
		--start-directory gen/tests \
		--pattern 'test_type_01_*.py' \
		--verbose
	@PYTHONPATH=gen/src $(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/contracts \
		--pattern 'test_type01*.py' \
		--verbose
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/intake:legacy/postgres:validation/oracle \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/unit \
		--pattern 'test_type01*.py' \
		--verbose
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/intake:legacy/postgres:validation/oracle \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory validation/oracle/tests \
		--pattern 'test_type01*.py' \
		--verbose
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/intake:legacy/postgres:validation/oracle \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/security \
		--pattern 'test_worker_security.py' \
		--verbose
	@$(MAKE) --no-print-directory test-java
	@docker compose config --quiet
	@PYTHONPATH=legacy/runner:legacy/publisher:legacy/postgres \
		$(RUNNER_PYTHON) -m unittest discover \
		--start-directory tests/postgres \
		--pattern 'test_type01*.py' \
		--verbose
	@$(RUNNER_PYTHON) tests/end-to-end/run_type01_suite.py

publish: ## Publish exactly one BATCH or BUNDLE through real SFTP.
	@test -n "$(BATCH)$(BUNDLE)" || { echo "set exactly one of BATCH=<batch-id> or BUNDLE=<directory>" >&2; exit 2; }
	@test -z "$(BATCH)" || test -z "$(BUNDLE)" || { echo "BATCH and BUNDLE are mutually exclusive" >&2; exit 2; }
	@$(RUNNER_PYTHON) legacy/runner/publish_raw_cli.py \
		"$(if $(BUNDLE),$(BUNDLE),$(OUTPUT)/$(BATCH))"

publish-raw: publish ## Compatibility alias for publish.

run: ## Run one typed scenario, or the same scenario for all five types.
	@case "$(TYPE)" in 01|02|03|04|05|all) ;; \
		*) echo "TYPE must be one of 01, 02, 03, 04, 05, or all" >&2; exit 2 ;; \
	esac
	@if [ "$(TYPE)" = "all" ]; then \
		for type_number in $(SUPPORTED_TYPES); do \
			$(RUNNER_PYTHON) legacy/runner/run_type.py \
				--type "$$type_number" \
				--scenario "$(SCENARIO)" || exit $$?; \
		done; \
	else \
		$(RUNNER_PYTHON) legacy/runner/run_type.py \
			--type "$(TYPE)" \
			--scenario "$(SCENARIO)"; \
	fi

run-type: run ## Compatibility alias for run.

run-file: ## Run one explicit typed FILE with sibling checksum and manifest.
	@case "$(TYPE)" in 01|02|03|04|05) ;; \
		*) echo "TYPE for run-file must be one of 01, 02, 03, 04" >&2; exit 2 ;; \
	esac
	@test -n "$(FILE)" || { echo "set FILE=<raw-file-path>" >&2; exit 2; }
	@$(RUNNER_PYTHON) legacy/runner/run_type.py \
		--type "$(TYPE)" \
		--file "$(FILE)"

worker: ## Run the automatic manifest-ready worker in the foreground.
	@$(RUNNER_PYTHON) legacy/runner/worker.py \
		--poll-interval "$(POLL_INTERVAL)" \
		--max-batches "$(MAX_BATCHES)" \
		--evidence-root "$(EVIDENCE)"

worker-once: ## Run exactly one bounded worker polling iteration.
	@$(RUNNER_PYTHON) legacy/runner/worker.py \
		--once \
		--poll-interval "$(POLL_INTERVAL)" \
		--max-batches "$(MAX_BATCHES)" \
		--evidence-root "$(EVIDENCE)"

test-e2e: ## Run the selected live acceptance suite; TYPE=all runs 01 through 05.
	@case "$(TYPE)" in 01|02|03|04|05|all) ;; \
		*) echo "TYPE must be one of 01, 02, 03, 04, 05, or all" >&2; exit 2 ;; \
	esac
	@if [ "$(TYPE)" = "all" ]; then \
		for type_number in $(SUPPORTED_TYPES); do \
			$(RUNNER_PYTHON) \
				"tests/end-to-end/run_type$${type_number}_suite.py" \
				|| exit $$?; \
		done; \
	else \
		$(RUNNER_PYTHON) \
			"tests/end-to-end/run_type$(TYPE)_suite.py"; \
	fi

test-worker-e2e: ## Run the live automatic-worker acceptance suite on a clean runtime.
	@$(RUNNER_PYTHON) "$(WORKER_E2E_SUITE)"

test: check test-postgres ## Run source/build, rollback-only PostgreSQL, and fresh worker acceptance.
	@$(RUNNER_PYTHON) "$(WORKER_E2E_SUITE)"

df-manifest: ## Recompute the legacy implementation manifest; REV=<rev> for a ledger entry.
	@$(RUNNER_PYTHON) factory/tools/tree_manifest.py \
		$(if $(REV),--rev "$(REV)",)

df-check: ## Run Dark Factory contract, unit, and security suites plus strict typing.
	@PYTHONPATH=$(DF_SRC) $(RUNNER_PYTHON) -m unittest discover \
		--start-directory factory/tests/contract \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=$(DF_SRC):factory/tests/unit $(RUNNER_PYTHON) -m unittest discover \
		--start-directory factory/tests/unit \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=$(DF_SRC) $(RUNNER_PYTHON) -m unittest discover \
		--start-directory factory/tests/security \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=$(DF_SRC) $(RUNNER_PYTHON) -m mypy \
		--python-version 3.12 \
		--strict \
		--no-incremental \
		factory/src \
		factory/tools/tree_manifest.py
	@$(RUNNER_PYTHON) -m json.tool factory/contracts/finding.schema.json >/dev/null
# The acceptance suite is not in the mypy scope, so a stale import in it can
# survive every other gate. Executing --help resolves every module it needs.
	@PYTHONPATH=$(DF_SRC) $(RUNNER_PYTHON) $(DF_SUITE) --help >/dev/null

df-detect: ## Run the detector for one TYPE against a deployed legacy runtime.
	@case "$(TYPE)" in 01|02|03|04|05) ;; \
		*) echo "TYPE for df-detect must be one of 01, 02, 03, 04" >&2; exit 2 ;; \
	esac
	@test -n "$(LEGACY_EVIDENCE)" || { echo "set LEGACY_EVIDENCE=<path>" >&2; exit 2; }
	@PYTHONPATH=$(DF_SRC) $(RUNNER_PYTHON) -m cli \
		--type "$(TYPE)" \
		--legacy-evidence-root "$(LEGACY_EVIDENCE)" \
		--evidence-root "$(DF_EVIDENCE)"

df-accept: ## Run the live Dark Factory acceptance gate for one TYPE or all four.
	@case "$(TYPE)" in 01|02|03|04|05|all) ;; \
		*) echo "TYPE must be one of 01, 02, 03, 04, 05, or all" >&2; exit 2 ;; \
	esac
	@$(RUNNER_PYTHON) $(DF_SUITE) \
		--type "$(TYPE)" \
		--legacy-evidence-root "$(if $(LEGACY_EVIDENCE),$(LEGACY_EVIDENCE),$(DF_DEFAULT_ROOTS))" \
		--evidence-root "$(DF_EVIDENCE)"

retool: ## Retool the line for a docked type: print the work order and the gates.
	@test -d "spec/type-$(TYPE)-"* 2>/dev/null || { \
		echo "no docked kit for TYPE=$(TYPE) under spec/" >&2; exit 2; }
	@echo "=============================================================="
	@echo " RETOOL  —  type $(TYPE)"
	@echo "=============================================================="
	@echo
	@echo "The line is being retooled for a new part. The kit is docked in"
	@echo "spec/ and is NOT installed. Nothing downstream of the sanitized"
	@echo "CSV exists for this type."
	@echo
	@ls -1 spec/type-$(TYPE)-*/
	@echo
	@echo "  declarative only — no code is delivered"
	@echo
	@echo "--- current state -------------------------------------------"
	@printf "  modern verticals built : "
	@ls -1 modern/ingestion/src/northwind_pay/types/ 2>/dev/null \
		| grep -c '^type' || echo 0
	@printf "  specification         : "
	@test -d "contracts/types/$(TYPE)-"* 2>/dev/null \
		&& echo "installed, legacy runs" || echo "MISSING"
	@printf "  modern vertical        : "
	@test -d "modern/ingestion/src/northwind_pay/types/type$(TYPE)_"* 2>/dev/null \
		&& echo "built" || echo "NOT BUILT  <- this is the job"
	@echo
	@echo "--- the loop ------------------------------------------------"
	@echo "  act    : make run / make modern-run / make modern-dbt"
	@echo "  observe: evidence/modern/<batch>/*.json"
	@echo "  gate   : golden-match resolved && unexplained_count == 0"
	@echo "  halt   : privacy leak | frozen write | unpassable gate"
	@echo
	@echo "--- work order ----------------------------------------------"
	@cat spec/type-$(TYPE)-*/WORK-ORDER.md

modern-init: ## Create the modern virtual environment from pinned requirements.
	@$(PYTHON) -m venv $(MODERN_VENV)
	@$(MODERN_PYTHON) -m pip install --quiet --upgrade pip
	@$(MODERN_PYTHON) -m pip install --quiet -r modern/requirements.txt
	@echo "modern environment initialized"

modern-check: ## Run modern unit, contract, and privacy suites plus strict typing.
	@PYTHONPATH=$(MODERN_SRC) $(MODERN_PYTHON) -m unittest discover \
		--start-directory tests/modern \
		--pattern 'test_*.py' \
		--verbose
	@PYTHONPATH=$(MODERN_SRC) $(MODERN_PYTHON) -m mypy \
		--python-version 3.12 \
		--strict \
		--no-incremental \
		$(MODERN_SRC)/northwind_pay

modern-run: ## Run the modern pipeline for one TYPE, closing golden-match.
	@case "$(TYPE)" in 01|02|03|04|05) ;; \
		*) echo "TYPE must be one of 01, 02, 03, 04, or 05" >&2; exit 2 ;; \
	esac
	@$(MODERN_PYTHON) modern/pipeline.py --type "$(TYPE)" $(MODERN_RUN_FLAGS)

modern-dbt: ## Build and test the modern Bronze, Silver, and Gold models.
	@cd modern/dbt && DBT_PROFILES_DIR=. ../.venv/bin/dbt build --no-use-colors

modern-rebuild: ## Rebuild the lakehouse from the immutable landing Parquet tree.
	@rm -rf $(MODERN_DUCKDB) .runtime/dlt .runtime/dbt
	@$(MODERN_PYTHON) modern/pipeline.py --type "$(if $(TYPE),$(TYPE),01)" $(MODERN_RUN_FLAGS)

modern-dagster: ## Materialize the modern assets through Dagster.
	@mkdir -p .runtime/dagster
	@DAGSTER_HOME=$(CURDIR)/.runtime/dagster PYTHONPATH=modern/dagster \
		$(MODERN_VENV)/bin/dagster asset materialize \
		-m northwind_modern_dagster --select '*' \
		--partition "$(if $(TYPE),$(TYPE),01)"

modern-api: ## Serve the read-only reconciliation API on 127.0.0.1:8099.
	@PYTHONPATH=modern/serving/api $(MODERN_VENV)/bin/uvicorn \
		app:application --host 127.0.0.1 --port 8099

clean: ## Delete disposable runtime state after explicit confirmation.
	@test "$(CONFIRM)" = "clean-runtime" || { echo "rerun with CONFIRM=clean-runtime" >&2; exit 2; }
	@docker compose down --volumes --remove-orphans
	@$(RUNNER_PYTHON) legacy/runner/clean_runtime.py

clean-runtime: clean ## Compatibility alias for clean.
