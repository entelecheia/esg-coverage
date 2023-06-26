import numpy as np
import pandas as pd


def preprocessing_esg_ratings(data: pd.DataFrame):
    # Define a mapping from ratings to numerical scores
    rating_map = {"A+": 6, "A": 5, "B+": 4, "B": 3, "C": 2, "D": 1, np.nan: np.nan}

    # Convert rating columns into numerical scores
    for year in range(2011, 2021):
        data[str(year)] = data[str(year)].map(rating_map)

    # Melt dataframe to have years as rows instead of columns
    melted_df = data.melt(
        id_vars=["type", "code", "name", "market"],
        var_name="year",
        value_name="rating_score",
        value_vars=[str(year) for year in range(2011, 2021)],
    )

    # Convert year to integer
    melted_df["year"] = melted_df["year"].astype(int)

    # Sort by type, code and year
    melted_df.sort_values(["type", "code", "year"], inplace=True)

    # Calculate rating change
    melted_df["rating_change"] = melted_df.groupby(["type", "code"])[
        "rating_score"
    ].diff()

    # Create 'rating' column by mapping numerical scores back to ratings
    reverse_rating_map = {v: k for k, v in rating_map.items()}
    melted_df["rating"] = melted_df["rating_score"].map(reverse_rating_map)

    # Set rating_change values to '1', '0', '-1' based on whether it's positive, zero or negative
    melted_df["rating_change"] = melted_df["rating_change"].apply(
        lambda x: 1 if x > 0 else (0 if x == 0 else (-1 if x < 0 else np.nan))
    )
    return melted_df


def preprocessing_esg_coverage(data: pd.DataFrame):
    data = data[data["year"] >= 2011]

    # Pivot the dataframe
    pivot_df = data.pivot(
        index=["code", "year"], columns="topic_num", values="topic_weight"
    ).reset_index()

    # Fill na values with 0
    pivot_df.fillna(0, inplace=True)

    # Define new categories
    pivot_df["E"] = pivot_df["topic0"]
    pivot_df["S"] = pivot_df["topic1"]
    pivot_df["G"] = pivot_df["topic2"] + pivot_df["topic6"]
    pivot_df["G2"] = pivot_df["topic2"]
    pivot_df["ESG"] = pivot_df["E"] + pivot_df["S"] + pivot_df["G"]
    pivot_df["ESG2"] = pivot_df["E"] + pivot_df["S"] + pivot_df["G2"]

    # Reset the column name
    pivot_df.columns.name = ""

    # Melt the dataframe to have types as rows instead of columns
    melted_df = pivot_df.melt(
        id_vars=["code", "year"],
        var_name="type",
        value_name="topic_weight",
        value_vars=["E", "S", "G", "G2", "ESG", "ESG2"],
    )

    # Calculate yearly changes in 'topic_weight' for each company and type
    melted_df["yearly_change"] = melted_df.groupby(["code", "type"])[
        "topic_weight"
    ].diff()

    # Calculate standard deviation of the yearly changes for each type
    type_std_devs = melted_df.groupby("type")["yearly_change"].std()

    # Initialize 'coverage_change' to NaN where 'yearly_change' is NaN
    melted_df["coverage_change"] = np.where(
        melted_df["yearly_change"].isna(), np.nan, 0
    )

    # Update 'coverage_change' based on 'yearly_change' relative to the standard deviation for the type
    for type in type_std_devs.index:
        std_dev = type_std_devs[type]
        type_mask = melted_df["type"] == type
        melted_df.loc[
            type_mask & (melted_df["yearly_change"] > 0.3 * std_dev), "coverage_change"
        ] = 1
        melted_df.loc[
            type_mask & (melted_df["yearly_change"] < -0.3 * std_dev), "coverage_change"
        ] = -1

    return melted_df
