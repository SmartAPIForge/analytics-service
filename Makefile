PIP := venv/scripts/pip
PYTHON3 := venv/scripts/python

venv:
	python -m venv venv

requirements:
	${PIP} install -r requirements.txt

migrate:
	${PYTHON3} manage.py makemigrations
	${PYTHON3} manage.py migrate

run:
	${PYTHON3} analytics_service/manage.py runserver