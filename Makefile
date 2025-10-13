PROJECT := football_es
CONDA := conda
ENV_FILE := environment.yml

# Met à jour l'environnement conda à partir du fichier environment.yml
conda-env-update:
	$(CONDA) env update -f $(ENV_FILE)
	@echo "✅ Environnement conda mis à jour!"
