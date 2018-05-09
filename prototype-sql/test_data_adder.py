import prototype_sql as pt
import pandas as pd

df = pd.read_csv("/Users/gustavo/Development/SIMSSA-database/test-data/Josquin + La Rue Mass duos Inventory - Sheet1.csv")


for index, row in df.iterrows():
    print(index, row['Composer'], row['Mass'])