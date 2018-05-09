import prototype_sql as pt
import pandas as pd

df = pd.read_csv("/Users/gustavo/Development/SIMSSA-database/prototype-sql/test-data/Josquin\ +\ La\ Rue\ Mass\ duos\ Inventory\ -\ Sheet1.csv")

print(df[['Composer', 'Mass']])