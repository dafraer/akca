push:
	git add . && git commit -m = '$(m)' && git push
run:
	python3 -m akca
venv:
	python3 -m venv ./.venv
	python3 -m venv ./.venv
	./.venv/bin/pip install -r requirements.txt