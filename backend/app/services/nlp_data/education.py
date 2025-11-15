import pandas as pd
import re

csv_path = r"C:\Users\leibn\Downloads\us-colleges-and-universities.csv\us-colleges-and-universities.csv"
# let pandas handle quoted strings
df = pd.read_csv(csv_path, quotechar='"', engine='python', sep=None)
print(df.head())
uni_names = df["NAME"]
#uni_sites = df["WEBSITE"]

list_of_universities = []

def get_universities():
    for name in uni_names:
        list_of_universities.append(str(name))
    return list_of_universities
"""
    for site in uni_sites:
        match = re.search(r"www\.([^.]+)\.", site)
        if match == None:
            continue
        else:
            list_of_universities.append(match.group(1))
"""

if __name__=="__main__":
    print(get_universities())