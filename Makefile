run3:
	python3 main.py

run2:
	python main.py

clean:
	find . -name '*.pyc' -exec rm --force {} +
