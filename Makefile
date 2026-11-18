.PHONY: example test

example:
	PYTHONPATH=src python3 -m risk_language

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v


.PHONY: evidence figures
evidence:
	PYTHONPATH=src python3 research/sweep.py

figures: evidence
	python3 research/figures.py
