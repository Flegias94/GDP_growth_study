import pandas as pd
import unicodedata
import pycountry_convert as pc


df_gdp = pd.read_csv("data/gdp_set.csv")
df_pop = pd.read_csv("data/pop_data.csv", sep=",", engine="python")

gdp_countries = set(df_gdp["Country"])
pop_countries = set(df_pop["Country"])


def canonicalize(name: str) -> str:
    if pd.isna(name):
        return name
    s = str(name).strip()  # trim spaces (e.g., "Brunei ")
    s = unicodedata.normalize("NFKD", s)  # split accents
    s = s.encode("ascii", "ignore").decode()  # remove accents (Cote dIvoire)
    s = s.replace("&", "and")
    s = s.replace("St.", "Saint")
    s = s.replace("St ", "Saint ")
    s = s.replace("  ", " ")
    return s


df_gdp["Country_clean"] = df_gdp["Country"].apply(canonicalize)
df_pop["Country_clean"] = df_pop["Country"].apply(canonicalize)


def get_region(country):
    try:
        country_code = pc.country_name_to_country_alpha2(country)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except:
        return None


df_gdp["Region"] = df_gdp["Country_clean"].apply(get_region)

name_map = {
    "Bahamas, The": "Bahamas",
    "Brunei Darussalam": "Brunei",
    "Cabo Verde": "Cape Verde",
    "Congo, Dem. Rep.": "Democratic Republic of the Congo",
    "Congo, Rep.": "Republic of the Congo",
    "Cote d'Ivoire": "Ivory Coast",
    "Czechia": "Czech Republic",
    "Egypt, Arab Rep.": "Egypt",
    "Gambia, The": "Gambia",
    "Hong Kong SAR, China": "Hong Kong",
    "Iran, Islamic Rep.": "Iran",
    "Korea, Rep.": "South Korea",
    "Korea, Dem. People's Rep.": "North Korea",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Lao PDR": "Laos",
    "Macao SAR, China": "Macau",
    "Micronesia, Fed. Sts.": "Federated States of Micronesia",
    "Russian Federation": "Russia",
    "Puerto Rico (US)": "Puerto Rico",
    "Sao Tome and Principe": "Sao Tome and Principe",
    "Slovak Republic": "Slovakia",
    "Syrian Arab Republic": "Syria",
    "Turkiye": "Turkey",
    "Venezuela, RB": "Venezuela",
    "Viet Nam": "Vietnam",
    "West Bank and Gaza": "Palestine",
    "Yemen, Rep.": "Yemen",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Lucia": "Saint Lucia",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    # (Leave “Puerto Rico (US)” unmapped if GDP uses “Puerto Rico” and you want to include it; otherwise it will be dropped by the intersection filter below.)
}
df_pop["Country_clean"] = df_pop["Country_clean"].replace(name_map)

gdp_countries = set(df_gdp["Country_clean"])
pop_countries = set(df_pop["Country_clean"])
extras_in_pop = pop_countries - gdp_countries
extras_in_gdp = gdp_countries - pop_countries

# print("Extras in Population dataset: ", len(extras_in_pop))
# print(sorted(list(extras_in_pop)))

# print("Extras in GDP dataset:", len(extras_in_gdp))
# print(sorted(list(extras_in_gdp)))

df_gdp_long = df_gdp.melt(
    id_vars=["Country_clean"],
    value_vars=["2020", "2021", "2022", "2023", "2024", "2025"],
    var_name="Year",
    value_name="GDP",
)
df_gdp_long["Year"] = df_gdp_long["Year"].astype(int)

year_cols = [str(y) for y in range(2020, 2025) if str(y) in df_pop.columns]

df_pop_long = df_pop.melt(
    id_vars=["Country_clean"],
    value_vars=year_cols,
    var_name="Year",
    value_name="Population",
)
df_pop_long["Year"] = df_pop_long["Year"].astype(int)

df_merged = pd.merge(
    df_gdp_long,
    df_pop_long,
    on=["Country_clean", "Year"],
    how="inner",  # only keep overlap
)

df_merged["GDP_per_capita"] = (df_merged["GDP"] * 1e6) / df_merged["Population"]

df_merged["Rank_pc"] = df_merged.groupby("Year")["GDP_per_capita"].rank(
    ascending=False, method="min"
)


ranks = df_merged[df_merged["Year"].isin([2020, 2023])]
ranks_pivot = ranks.pivot(index="Country_clean", columns="Year", values="Rank_pc")
ranks_pivot["RankChange_20_23"] = ranks_pivot[2020] - ranks_pivot[2023]
# print(
#     ranks_pivot.sort_values("RankChange_20_23", ascending=False).head(10).round(2)
# )  # biggest climbers
# print(ranks_pivot.sort_values("RankChange_20_23").head(10).round(2))  # biggest fallers

pc = df_merged.pivot(index="Country_clean", columns="Year", values="GDP_per_capita")
pc["pc_growth_abs_20_23"] = pc[2023] - pc[2020]
pc["pc_growth_pct_20_23"] = (pc["pc_growth_abs_20_23"] / pc[2020]) * 100
# print(pc.sort_values("pc_growth_pct_20_23", ascending=False).head(10).round(2))


# attach Region once (from your cleaned GDP table)
df_region = df_gdp[["Country_clean", "Region"]].drop_duplicates()
df_merged = df_merged.merge(df_region, on="Country_clean", how="left")

# avg per-capita by region and year
region_pc = (
    df_merged.groupby(["Region", "Year"])["GDP_per_capita"].mean().unstack("Year")
)
# print(region_pc.round(2))

df_merged.to_csv("data/out/gdp_population_per_capita_long.csv", index=False)


import matplotlib.pyplot as plt

# top10_2023 = df_merged[df_merged["Year"] == 2023].nlargest(10, "GDP_per_capita")[
#     ["Country_clean", "GDP_per_capita"]
# ]

# plt.figure(figsize=(8, 6))
# plt.barh(top10_2023["Country_clean"], top10_2023["GDP_per_capita"])
# plt.gca().invert_yaxis()
# plt.xlabel("GDP per capita (USD)")
# plt.title("Top 10 GDP per capita — 2023")
# plt.savefig(
#     "charts/Top 10 GDP per capita — 2023.png",
#     dpi=150,
#     bbox_inches="tight",
# )
# plt.tight_layout()
# plt.show()

# bottom10_2023 = df_merged[df_merged["Year"] == 2023].nsmallest(10, "GDP_per_capita")[
#     ["Country_clean", "GDP_per_capita"]
# ]

# plt.figure(figsize=(8, 6))
# plt.barh(bottom10_2023["Country_clean"], bottom10_2023["GDP_per_capita"])
# plt.gca().invert_yaxis()
# plt.xlabel("GDP per capita (USD)")
# plt.title("Bottom 10 GDP per capita — 2023")
# plt.savefig(
#     "charts/Bottom 10 GDP per capita — 2023.png",
#     dpi=150,
#     bbox_inches="tight",
# )
# plt.tight_layout()
# plt.show()


# If you already created region_pc as a table Region x Year with mean GDP_per_capita:
# plt.figure(figsize=(9, 6))
# for region, row in region_pc.iterrows():
#     plt.plot(row.index, row.values, label=region)

# plt.title("Average GDP per capita by Region (2020–2024)")
# plt.savefig(
#     "charts/Average GDP per capita by Region (2020–2024).png",
#     dpi=150,
#     bbox_inches="tight",
# )
# plt.xlabel("Year")
# plt.ylabel("GDP per capita (USD)")
# plt.legend()
# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(8, 5))
# plt.hist(df_merged.loc[df_merged["Year"] == 2023, "GDP_per_capita"].dropna(), bins=25)
# plt.xlabel("GDP per capita (USD)")
# plt.ylabel("Number of countries")
# plt.title("Distribution of GDP per capita — 2023")
# plt.savefig(
#     "charts/Distribution of GDP per capita — 2023", dpi=150, bbox_inches="tight"
# )
# plt.tight_layout()
# plt.show()


# subset_2023 = df_merged[df_merged["Year"] == 2023]

# plt.figure(figsize=(7, 6))
# plt.scatter(subset_2023["GDP"] * 1e6, subset_2023["GDP_per_capita"])
# plt.xscale("log")  # GDP spans orders of magnitude
# plt.xlabel("GDP (USD, log scale)")
# plt.ylabel("GDP per capita (USD)")
# plt.title("Country GDP vs GDP per capita — 2023")
# plt.savefig("charts/Country GDP vs GDP per capita — 2023", dpi=150, bbox_inches="tight")
# plt.tight_layout()
# plt.show()


# # biggest climbers
# gain = ranks_pivot.sort_values("RankChange_20_23", ascending=False).head(10)
# plt.figure(figsize=(8, 5))
# plt.barh(gain.index, gain["RankChange_20_23"])
# plt.gca().invert_yaxis()
# plt.xlabel("Rank improvement (2020 → 2023)")
# plt.title("Biggest rank climbers (GDP per capita)")
# plt.savefig("charts/Big climbers", dpi=150, bbox_inches="tight")
# plt.tight_layout()
# plt.show()
# # biggest fallers
# fall = ranks_pivot.sort_values("RankChange_20_23").head(10)
# plt.figure(figsize=(8, 5))
# plt.barh(fall.index, -fall["RankChange_20_23"])  # make positive bars for readability
# plt.gca().invert_yaxis()
# plt.xlabel("Rank decline (2020 → 2023)")
# plt.title("Biggest rank decliners (GDP per capita)")
# plt.savefig("charts/Big fallers", dpi=150, bbox_inches="tight")
# plt.tight_layout()
# plt.show()
