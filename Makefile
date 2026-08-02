.PHONY: review-packet test check-planning-brief check-proof check-work finish-work validate-examples doctor kickoff kickoff-build triage-review-finding export-skill skill-budget local-ready public-ready pevie-test pevie-review-packet pevie-validate-examples pevie-design-lint test-all

PROFILE ?= both
MODE ?= package
STACK ?= generic
OUT ?= .dist/pjario-staltman-skill
SKILL_MODE ?= standard
DECISION ?= test

review-packet:
	python3 tools/review-packet.py --include-untracked --output .review-packet.md

test:
	python3 -m unittest discover -s tests -p "test_*.py"

pevie-test:
	python3 -m unittest discover -s "Pevie Hischer/tests" -p "test_*.py"

pevie-review-packet:
	$(MAKE) -f "Pevie Hischer/Makefile" review-packet

validate-examples:
	python3 tools/pjario.py finish --packet examples/work-packets/trivial-copy.md >/dev/null
	python3 tools/pjario.py finish --packet examples/work-packets/non-trivial-integration.md >/dev/null
	python3 tools/check-planning-brief.py --ticket examples/trivial-ticket.md
	python3 tools/check-planning-brief.py --ticket examples/non-trivial-ticket.md --planning-brief examples/planning-brief.md
	python3 tools/check-planning-brief.py --ticket examples/golden-workflow/ticket.md --planning-brief examples/golden-workflow/planning-brief.md
	python3 tools/check-proof.py --ticket examples/golden-workflow/ticket.md --qa-plan examples/golden-workflow/qa-plan.md --pr-note examples/golden-workflow/pr-note.md --completion-report examples/golden-workflow/completion-report.md

pevie-validate-examples:
	$(MAKE) -f "Pevie Hischer/Makefile" validate-examples

pevie-design-lint:
	$(MAKE) -f "Pevie Hischer/Makefile" design-lint-examples

doctor:
	python3 tools/doctor.py --mode "$(MODE)" --profile "$(PROFILE)" --stack "$(STACK)" --public-ready

kickoff:
	@if [ -z "$(TICKET)" ]; then \
		echo "TICKET is required"; \
		exit 2; \
	fi
	python3 tools/kickoff.py --profile "$(if $(filter both,$(PROFILE)),core,$(PROFILE))" --ticket "$(TICKET)" $(if $(PLAN),--planning-brief "$(PLAN)") $(if $(DESIGN),--design "$(DESIGN)")

kickoff-build:
	@if [ -z "$(REQUEST)" ]; then \
		echo "REQUEST is required"; \
		exit 2; \
	fi
	python3 tools/kickoff.py --profile "$(if $(filter both,$(PROFILE)),core,$(PROFILE))" --build-request "$(REQUEST)"

triage-review-finding:
	@if [ -z "$(FINDING)" ]; then \
		echo "FINDING is required"; \
		exit 2; \
	fi
	python3 tools/triage-review-finding.py --finding "$(FINDING)" --decision "$(DECISION)"

export-skill:
	python3 tools/export-skill.py --output "$(OUT)" --mode "$(SKILL_MODE)" --force

skill-budget:
	tmpdir="$$(mktemp -d)"; $(MAKE) export-skill OUT="$$tmpdir/standard" SKILL_MODE=standard; python3 tools/check-skill-budget.py --skill-dir "$$tmpdir/standard" --max-skill-words 220 --max-total-words 750
	tmpdir="$$(mktemp -d)"; $(MAKE) export-skill OUT="$$tmpdir/caveman" SKILL_MODE=caveman; python3 tools/check-skill-budget.py --skill-dir "$$tmpdir/caveman" --max-skill-words 140 --max-total-words 140

test-all: test pevie-test validate-examples pevie-validate-examples

local-ready: test-all doctor
	git diff --check
	$(MAKE) kickoff-build REQUEST=examples/golden-workflow/build-request.md >/tmp/pjario-staltman-kickoff.md
	python3 tools/pjario.py adopt --target . --profile core --dry-run >/tmp/pjario-staltman-adopt.md
	$(MAKE) skill-budget
	tmpdir="$$(mktemp -d)"; $(MAKE) export-skill OUT="$$tmpdir/pjario-staltman"
	$(MAKE) review-packet
	$(MAKE) pevie-review-packet
	rm -f .review-packet.md "Pevie Hischer/.review-packet.md"

public-ready: local-ready
	$(MAKE) pevie-design-lint

check-planning-brief:
	@if [ -n "$(PLAN)" ]; then \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)" --planning-brief "$(PLAN)"; \
	else \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)"; \
	fi

check-proof:
	@if [ -n "$(PACKET)" ]; then \
		python3 tools/check-proof.py --packet "$(PACKET)"; \
	else \
		python3 tools/check-proof.py --ticket "$(TICKET)" --qa-plan "$(QA)" --pr-note "$(PR)" $(if $(COMPLETION),--completion-report "$(COMPLETION)"); \
	fi

check-work:
	python3 tools/pjario.py check --packet "$(PACKET)"

finish-work:
	python3 tools/pjario.py finish --packet "$(PACKET)"
