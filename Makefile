run:
	uvicorn main:app & traefik/traefik --configFile=traefik/traefik.toml
run_dev:
	uvicorn main:app --reload & traefik/traefik --configFile=traefik/traefik.toml