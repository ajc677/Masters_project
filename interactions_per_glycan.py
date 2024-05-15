import pandas as pd

Hudson_matches = pd.read_csv('hudson_matches.csv',low_memory=False)
Plevin_matches = pd.read_csv('plevin_matches.csv',low_memory=False)

unique_interactions_hudson = {"PDB":[],"TSChainID":[],"ID":[],"Count":[],"G_Type":[],"G_Size":[]}
unique_interactions_plevin = {"PDB":[],"TSChainID":[],"ID":[],"Count":[],"G_Type":[],"G_Size":[]}

def process_data(csv,output):
    for count_A,PDB_ID_A in enumerate(csv["FileName"]):
        match = False

        for count_B,PDB_ID_B in enumerate(output["PDB"]):
            if PDB_ID_A == PDB_ID_B:
                if output["TSChainID"][count_B] == csv["TSChainId"][count_A]:
                    match = True
                    break
            
        if match == True:
            output["Count"][count_B] += 1
            continue
            
        else:
            output["PDB"].append(PDB_ID_A)
            output["TSChainID"].append(csv["TSChainId"][count_A])
            output["ID"].append(csv["ID"][count_A])
            output["Count"].append(1)
            output["G_Type"].append(csv["Results"][count_A])
            output["G_Size"].append(csv["GlycanSize"][count_A])
            continue

if __name__ == "__main__":
    process_data(Hudson_matches,unique_interactions_hudson)
    df = pd.DataFrame(unique_interactions_hudson)
    df.to_csv("hudson_total.csv")

    process_data(Plevin_matches,unique_interactions_plevin)
    df = pd.DataFrame(unique_interactions_plevin)
    df.to_csv("plevin_total.csv") 
