from sqlalchemy import create_engine
import pandas as pd
from pg_link import PG_LINK

engine = create_engine(PG_LINK)

# Assuming your JSON data is stored in a file named 'data.json'
df = pd.read_json("data.json")

# Now, df is a DataFrame containing your JSON data as a table
# print(df)

df.to_sql("amazon_reviews", engine, if_exists="replace", index=False)
print("Data uploaded successfully.")
