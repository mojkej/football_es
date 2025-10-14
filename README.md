# football_es

We will analyze Spanish league data from 2012 to 2021. These data were taken from [Football CSV](https://footballcsv.github.io). We will transform the data to combine them into a single dataframe for later analysis.

## Project summary / Résumé du projet

This repository implements an ETL pipeline and a Spark analysis notebook to aggregate Spanish league seasons (2012–2021). The pipeline:
- Recursively searches dataset folders for CSV files and excludes specific files (e.g. `transformed_data.csv`, `es.2.csv`).
- Extracts CSV data into pandas, applies robust transformation and writes a single `transformed_data.csv`.
- Logs progress and errors to `log_file.txt` with timestamps.

The Spark notebook (`football_es.ipynb`) loads `transformed_data.csv`, cleans and casts columns, computes match results, and aggregates statistics by team and season.

## What I changed / Ce que j'ai fait

- extract_transform_data.py
  - Recursive CSV discovery (search subfolders such as `datasets/2010s/2012-13`).
  - Safer CSV reading and tolerant parsing (handles missing/invalid files).
  - Robust date parsing (day-first, tolerant) and FT splitting into two score columns.
  - Numeric conversion of scores and a Result column (`Team 1 Win`, `Team 2 Win`, `Draw`, `Unknown`).
  - Improved logging format and skipping writes when no data.
- football_es.ipynb
  - Ensure Spark environment variables set (JAVA_HOME / SPARK_HOME).
  - Correct season computation: season start year is year if month >= July, otherwise previous year; Season label formatted `YYYY-YY` (e.g. `2012-13`).

## How to run / Comment exécution

1. Create a Python environment and install requirements:
   - pandas
   - python-dotenv
   - pyspark (if using notebook Spark)
   - findspark (optional)
2. Set environment variables in a `.env` file or your shell:
   - JAVA_HOME (path to JDK)
   - SPARK_HOME (path to Spark installation) — required for local Spark sessions
3. Run ETL (from repo root):
   - python extract_transform_data.py
   - This produces `transformed_data.csv` and appends logs to `log_file.txt`
4. Open `football_es.ipynb` with Jupyter / VSCode and run cells (ensure Spark dependencies and environment variables are correct).

## Known issues / Points d'attention

- Column name sensitivity: CSV headers must match exact column names used in code (`Team 1`, `Team 2`, `FT`, `Date`, etc.).  
- Spark connection errors (`Connection refused`) usually indicate wrong `SPARK_HOME` or `JAVA_HOME`, or Spark not installed; check environment and run `findspark.init()` if necessary. You can use google colab;
- Scores that contain unexpected characters are cleaned, but ambiguous entries may become `Unknown` or null.

## Next improvements / Améliorations futures

- Add unit tests for extract/transform functions.  
- Add CLI args to control input/output paths and exclusion lists.  
- Parallelize CSV extraction for very large datasets.  
- Add schema validation and explicit column typing before aggregation.

## Contact / Notes

If you still get errors, copy the full traceback and the problematic CSV example — that helps diagnosing exact parsing or casting issues.
