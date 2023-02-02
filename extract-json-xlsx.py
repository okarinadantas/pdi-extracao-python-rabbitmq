import pandas as pd

data = pd.read_json("queues-binds.json")
grouped_data = data.groupby(by=["destination", "source"]).sum()

grouped_data.to_excel("queues-binds.xlsx", engine="openpyxl")
