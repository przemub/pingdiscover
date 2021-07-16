SHELL := /bin/bash

.PHONY: help

help:   ## Lists commands and their purpose
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

system: ## Installs requirements using the system pip
	pip3 install aioping

venv:   ## Creates a venv and activates it
	python3 -m venv ping_venv
	source ping_venv/bin/activate && pip install aioping;
	bash -c "source ping_venv/bin/activate && exec $$BASH"

docker: ## Builds a Docker container
	docker build -t pingdiscover .

conda:  ## Creates and activates a Conda environment
	conda env create -f environment.yml
	bash -c "conda activate pingdiscover && exec $$BASH"

