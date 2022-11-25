run:
	uvicorn main:app & traefik/traefik --configFile=traefik/traefik.toml
run_dev:
	uvicorn main:app --reload & traefik/traefik --configFile=traefik/traefik.toml
setup_db:
	alembic upgrade 789894c92df0
	python3 database/seed.py