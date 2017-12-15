all:
	python main.py

clean:
	find . -name '*.pyc' -exec rm --force {} +
