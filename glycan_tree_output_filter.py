import pandas as pd

def process_data():
    raw_tree_type = pd.read_csv('glycan_tree_output.csv',low_memory=False)

    df = {"FileName":[],"TSChainId":[],"ID":[],"WURCS":[],"Results":[]}

    for y,x in enumerate(raw_tree_type["Unnamed: 0"]):

        if raw_tree_type["Results"][y] == "Sugar WURCS not recognised" or raw_tree_type["Results"][y] == "Error producing WURCS string":
            continue

        if "ASN" in raw_tree_type["ID"][y] and "NAG" in raw_tree_type["ID"][y]:
            for key in df:
                df[key].append(raw_tree_type[key][y])

    filtered_tree_type = pd.DataFrame(df)

    tree_type_no_duplicates = filtered_tree_type.drop_duplicates(subset=["FileName","TSChainId","ID","WURCS","Results"])

    tree_type_no_duplicates.to_csv("processed_tree_types.csv")

if __name__ == "__main__":
    process_data()
