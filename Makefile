venv:
	python -m venv venv && 
	. venv/bin/activate && pip install -r requirements.txt

show:
	. venv/bin/activate && saved_model_cli show --dir ml/models/commands/1 --all

build:
	docker compose build

run: 
	docker compose up