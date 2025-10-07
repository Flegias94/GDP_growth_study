import pandas as pd
import matplotlib.pyplot as plt
import pycountry_convert as pc
from sklearn.preprocessing import MinMaxScaler, StandardScaler


df = pd.read_csv("data/gdp_set.csv")


def classify_growth(x):
    if x < 0:
        return "Shrinking"
    elif x < 50:
        return "Moderate"
    else:
        return "High Growth"


# task 1
# print(df.shape)
# print(df.columns)
# print(df.head())

# task 2
# print(df.info())
# print(df.isna().sum())

# task 3
# print(df.describe())
# print(df["Country"].nunique())
# print(df["Country"].value_counts().head())

# task 4
# print(df.describe())
# print(df.sort_values(by="2020", ascending=False).head(1))
# print(df.sort_values(by="2025", ascending=False).head(1))

# task 5
df["Growth"] = df["2025"] - df["2020"]
df["GrowthRate"] = (df["2025"] - df["2020"]) / df["2020"] * 100
# print(df.sort_values(by="Growth", ascending=False).head(1))
# print(df.sort_values(by="GrowthRate", ascending=False).head(1))
# print(df.sort_values(by="GrowthRate", ascending=True).head(1))


# task 6
# print(df[df["2025"].isna()])
# print(df.sort_values(by="GrowthRate", ascending=False).head(10))
# print(df.sort_values(by="GrowthRate", ascending=True).head(10))

df["Country"] = df["Country"].str.strip()
# print(df["Country"].duplicated().sum())

# print(df.isna().sum())

# Level 2 — Exploratory Stats

# Median GDP vs. Mean GDP in 2020 and 2025 (does one rich country skew the average?).

# Top 5 by GDP per year: Loop through 2020–2025, find the leader each year.

# Volatility check: For each country, compute standard deviation across years. Who is most unstable?

# print(df["2020"].mean())
# print(df.loc[:, df.columns != "Country"].mean())

# idx = df["GrowthRate"].idxmax()
# idx1 = df["GrowthRate"].idxmin()

# df["RowMean"] = df.loc[:, "2020":"2025"].mean(axis=1)
# df["RowMedian"] = df.loc[:, "2020":"2025"].median(axis=1)

# idx_mean_max = df["RowMean"].idxmax()
# idx_mean_min = df["RowMean"].idxmin()

# idx_median_max = df["RowMedian"].idxmax()
# idx_median_min = df["RowMedian"].idxmin()
# # print(df.loc[idx_mean_max])
# # print(df.loc[idx_mean_min])
# # print(df.loc[idx_median_max])
# # print(df.loc[idx_median_min])

# top = df[["Country", "GrowthRate"]].nlargest(11, "GrowthRate").iloc[1:]
# bot = df[["Country", "GrowthRate"]].nsmallest(10, "GrowthRate")

# plt.bar(bot["Country"], bot["GrowthRate"])
# plt.ylabel("Growth Rate (%)")
# plt.title("Top 10 Slowest-Growing Economies")
# plt.show()

# df["RowMean"] = df.loc[:, "2020":"2025"].mean(axis=1)
# top5 = df.nlargest(5, "RowMean")

# years = ["2020", "2021", "2022", "2023", "2024", "2025"]

# for _, row in top5.iterrows():
#     plt.plot(years, row[years], label=row["Country"])

# plt.title("Top 5 Countries by Average GDP (2020–2025)")
# plt.xlabel("Year")
# plt.ylabel("GDP")
# plt.legend()
# plt.show()


# values = df["GrowthRate"]

# plt.hist(values, bins=20)

# plt.hist(df["GrowthRate"], bins=20, color="skyblue", edgecolor="black")
# plt.xlabel("Growth Rate (%)")
# plt.ylabel("Number of Countries")
# plt.title("Distribution of GDP Growth Rates (2020–2025)")
# plt.show()


# plt.scatter(df["2020"], df["GrowthRate"], color="green", alpha=0.5)
# plt.xscale("log")  # optional, to handle very large GDP differences
# plt.xlabel("GDP in 2020")
# plt.ylabel("Growth Rate (%)")
# plt.title("Relationship between Initial GDP (2020) and Growth Rate (2020–2025)")
# plt.show()


def country_to_continent(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except:
        return None


df["Region"] = df["Country"].apply(country_to_continent)
# region_growth = df.groupby("Region")["GrowthRate"].agg(["mean", "median", "min", "max"])
# print(region_growth)

# region_growth.plot(kind="bar", color="skyblue", edgecolor="black")
# plt.ylabel("Average Growth Rate (%)")
# plt.title("Average GDP Growth by Region (2020–2025)")
# plt.show()

# df.boxplot(column="GrowthRate", by="Region", grid=False)

# plt.title("Distribution of GDP Growth Rates by Region (2020–2025)")
# plt.suptitle("")  # remove automatic extra title
# plt.ylabel("Growth Rate (%)")
# # plt.show()

df_clean = df.dropna(subset=["2025"])

df_clean.loc[:, "GrowthCategory"] = df_clean["GrowthRate"].apply(classify_growth)

# counts = df_clean["GrowthCategory"].value_counts(ascending=True)
# plt.bar(counts.index, counts.values, color=["red", "orange", "green"])
# plt.title("Number of Countries by Growth Category")
# plt.xlabel("Growth Category")
# plt.ylabel("Number of Countries")
# plt.show()


# Level 3 — Transformations

# Growth categories:
# Add a label like "High Growth", "Decline", "Moderate" based on thresholds of GrowthRate.

# Normalize GDPs: Divide all values by 1,000,000 → work in trillions for readability.

# scaler_norm = MinMaxScaler()
# df_clean["GDP2020_norm"] = scaler_norm.fit_transform(df_clean[["2020"]])

# scaler_std = StandardScaler()
# df_clean["GDP2020_std"] = scaler_std.fit_transform(df_clean[["2020"]])

# print(df_clean[["Country", "2020", "GDP2020_norm", "GDP2020_std"]].head(10))

# Rank each country per year:

# df_clean["Rank2020"] = df_clean["2020"].rank(ascending=False, method="min").astype(int)
# print(df_clean[["Country", "2020", "Rank2020"]].sort_values("Rank2020").head(10))

# df_clean["Rank2025"] = df_clean["2025"].rank(ascending=False, method="min").astype(int)
# print(df_clean[["Country", "2025", "Rank2025"]].sort_values("Rank2025").head(10))

# df_clean["RankChange"] = df_clean["Rank2020"] - df_clean["Rank2025"]

# print("Top 10 Rank Gainers:")
# print(
#     df_clean.sort_values("RankChange", ascending=False).head(10)[
#         ["Country", "Rank2020", "Rank2025", "RankChange"]
#     ]
# )

# print("\nTop 10 Rank Losers:")
# print(
#     df_clean.sort_values("RankChange").head(10)[
#         ["Country", "Rank2020", "Rank2025", "RankChange"]
#     ]
# )


df_long = df_clean.melt(
    id_vars=["Country", "Region"],
    value_vars=["2020", "2021", "2022", "2023", "2024", "2025"],
    var_name="Year",
    value_name="GDP",
)

pivot = df_long.pivot_table(
    values="GDP", index="Region", columns="Year", aggfunc=["mean", "median"]
)
print(pivot.round(2))


pivot.loc[:, ("median", slice(None))].plot(kind="line")
plt.title("Median GDP per Region (2020–2025)")
plt.ylabel("GDP")
plt.show()

pivot.loc[:, ("mean", slice(None))].plot(kind="line")
plt.title("Mean GDP per Region (2020–2025)")
plt.ylabel("GDP")
plt.show()
