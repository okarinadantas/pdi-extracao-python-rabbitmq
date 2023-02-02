import pandas as pd

# Read json file
data = pd.read_json("queues-binds.json")

# Group data by queue and binds
grouped_data = data.groupby(by=["destination", "source"]).sum()

# Export as .xlsx
grouped_data.to_excel("queues-binds.xlsx", engine="openpyxl")
