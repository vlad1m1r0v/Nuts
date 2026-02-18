PYTHON = python3
MANAGE = nuts/manage.py
VITE_DIR = frontend

.PHONY: server worker beat frontend

server:
	$(PYTHON) $(MANAGE) runserver

worker:
	cd nuts && celery -A nuts worker -l info

beat:
	cd nuts && celery -A nuts beat -l info

frontend:
	cd $(VITE_DIR) && npm run dev