.PHONY: review-packet test check-planning-brief pevie-test pevie-review-packet test-all

review-packet:
	python3 tools/review-packet.py --include-untracked --output .review-packet.md

test:
	python3 -m unittest discover -s tests -p "test_*.py"

pevie-test:
	python3 -m unittest discover -s "Pevie Hischer/tests" -p "test_*.py"

pevie-review-packet:
	$(MAKE) -f "Pevie Hischer/Makefile" review-packet

test-all: test pevie-test

check-planning-brief:
	@if [ -n "$(PLAN)" ]; then \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)" --planning-brief "$(PLAN)"; \
	else \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)"; \
	fi
