.PHONY: install test benchmark
install:
	pip install -r requirements.txt
test:
	pytest tests/ -v
benchmark:
	python -m zkforge.cli benchmark --size 1048576
