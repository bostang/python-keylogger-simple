.PHONY: install run build lint fs co

install:
	pip install -r requirements.txt

run:
	python src/py-logger.py

lint:
	python src/lint-history.py

upload:
	python src/upload-to-github.py

# fs : find secrets
fs:
	python src/detect-secrets.py

build:
	pyinstaller --onefile --noconsole src/py-logger.py > log/build.log 2>&1
# 	pyinstaller --onefile --noconsole src/py-logger.py

# co : clean-output
co:
	@echo "Cleaning output logs..."
	@if exist output del /q output\cleaned\cleaned_typing_history*.txt
	@if exist output del /q output\raw\typing_history*.txt
