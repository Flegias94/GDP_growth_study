# GDP Growth and Per-Capita Analysis (2020–2025)

Practice data analysis project exploring GDP totals and GDP per capita across countries and regions from 2020 to 2025. The workflow covers cleaning, feature engineering (growth and growth rate), regional aggregation, ranking, and visualizations.

## Datasets
- `data/gdp_set.csv` – GDP by country for years 2020–2025 (values in millions of USD).
- `data/pop_data.csv` – Population by country for overlapping years.

## What’s included
- Data cleaning and canonicalization of country names.
- Growth metrics: absolute growth and growth rate (2020 → 2025).
- Region mapping (continents) and regional summaries.
- GDP per capita via GDP–population merge, with yearly ranks and rank changes.
- Visuals: distributions, top/bottom bar charts, regional trend lines, scatter of GDP vs GDP per capita.

## Tech stack
Python, pandas, matplotlib, scikit-learn (scalers), pycountry-convert/pycountry.

## Repository structure
analysis.ipynb # main notebook (recommended entry point)
analysis.py # script version of the analysis (optional)
data/
gdp_set.csv
pop_data.csv
charts/ # saved figures (created at run time)
outputs/ # saved tables (created at run time)
requirements.txt


## Quickstart
```bash
# clone
git clone https://github.com/Flegias94/GDP_growth_study.git
cd GDP_growth_study

# install deps
pip install -r requirements.txt
# or, if you prefer:
# pip install pandas matplotlib scikit-learn pycountry-convert pycountry

# open the notebook
jupyter notebook analysis.ipynb
# or run the script
python analysis.py
```
**Notebook guide (analysis.ipynb)**
1. Load and inspect data (shape, columns, missing values).
2. Compute Growth and GrowthRate from 2020 to 2025.
3. Map Country to Region (continent); summarize by region.
4. Merge GDP with population and compute GDP_per_capita.
5. Rank countries by GDP per capita per year; compute rank changes (2020 → 2023).
6.Visualize:
  - Distribution of growth rates and GDP per capita.
  - Top/bottom countries by GDP per capita in the latest year.
  - Regional mean/median trends by year.
  - Scatter: GDP vs GDP per capita (log-scaled GDP).

**Outputs**
Tables saved to outputs/ (e.g., regional summaries, rank changes).
Figures saved to charts/ (e.g., top 10 per-capita bar chart, region trends).

**Notes**

GDP values are treated as millions of USD unless otherwise noted.
If pycountry-convert fails for some names, a small manual mapping is applied inside the notebook/script

