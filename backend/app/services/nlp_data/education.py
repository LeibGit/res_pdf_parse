import pandas as pd

csv_path = r"C:\Users\leibn\Downloads\us-colleges-and-universities.csv\us-colleges-and-universities.csv"
# let pandas handle quoted strings
df = pd.read_csv(csv_path, quotechar='"', engine='python', sep=None)
uni_names = df["NAME"]

def get_universities():
    list_of_universities = []
    for name in uni_names:
        list_of_universities.append(str(name))
    return list_of_universities

if __name__=="__main__":
    print(get_universities())