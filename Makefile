.PHONY: review-packet test check-planning-brief validate-examples pevie-test pevie-review-packet pevie-validate-examples test-all

review-packet:
	python3 tools/review-packet.py --include-untracked --output .review-packet.md

test:
	python3 -m unittest discover -s tests -p "test_*.py"

pevie-test:
	python3 -m unittest discover -s "Pevie Hischer/tests" -p "test_*.py"

pevie-review-packet:
	$(MAKE) -f "Pevie Hischer/Makefile" review-packet

validate-examples:
	python3 tools/check-planning-brief.py --ticket examples/trivial-ticket.md
	python3 tools/check-planning-brief.py --ticket examples/non-trivial-ticket.md --planning-brief examples/planning-brief.md

pevie-validate-examples:
	$(MAKE) -f "Pevie Hischer/Makefile" validate-examples

test-all: test pevie-test validate-examples pevie-validate-examples

check-planning-brief:
	@if [ -n "$(PLAN)" ]; then \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)" --planning-brief "$(PLAN)"; \
	else \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)"; \
	fi
