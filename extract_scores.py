import requests
import pandas as pd

url = "https://www.inchcalculator.com/acft-calculator/#idx_how_to_calculate_an_acft_score"
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]
print(df)
df.to_csv('ACFT_STANDARDS.csv')