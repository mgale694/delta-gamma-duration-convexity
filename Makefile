.PHONY: example test

example:
	PYTHONPATH=src python3 -m risk_language

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

