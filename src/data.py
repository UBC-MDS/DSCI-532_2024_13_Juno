import pandas as pd

df = pd.read_csv("data/raw/filtered_canada.csv")

new_df = df[(df["Size of enterprise"] == "Total all sizes") &
            (df["Unit of measure"] == "Number") &
            (df["Executive"] == "All officers\xa0") &
            (df["GEO"] != "Unclassified province or territory")
].copy()
new_df = new_df.loc[:, ["REF_DATE", "Gender", "GEO", "VALUE", "Industry", "Type of corporation"]]

new_df.to_csv('data/filtered/filtered_data.csv', index=False)

df = pd.read_csv('data/filtered/filtered_data.csv')

