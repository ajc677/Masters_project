import pandas as pd

tree_types = pd.read_csv('tree_types_corrected.csv',low_memory=False)
hudson_csv = pd.read_csv('hudson_processed.csv',low_memory=False)
plevin_csv = pd.read_csv('plevin_processed.csv',low_memory=False)

hudson_interactions = {"FileName":[],"TotalGlycansInModel":[],"GlycanSize":[],"TSChainId":[],"ID":[],"TSType":[],"TSSeqnum":[],"TSC_Atom":[],"TSH_Atom":[],"WURCS":[],"Results":[]}
plevin_interactions = {"FileName":[],"TotalGlycansInModel":[],"GlycanSize":[],"TSChainId":[],"ID":[],"TSType":[],"TSSeqnum":[],"TSC_Atom":[],"TSH_Atom":[],"WURCS":[],"Results":[]}


def match_search(csv,output):
    from_tree_types = ["FileName","TSChainId","ID","WURCS","Results"]
    from_XHpi = ["glycanSize","targetSugar_target_sugar_type","targetSugar_target_sugar_seqnum","targetSugar_target_sugar_c_atom","targetSugar_target_sugar_h_atom","totalGlycansInModel"]
    XHpi_rename = ["GlycanSize","TSType","TSSeqnum","TSC_Atom","TSH_Atom","TotalGlycansInModel"]

    #loops through glycan tree types with count
    for count_A,PDB_A in enumerate(csv["PDB"]):
        print(f"{count_A}/24425")

        #loops through XHpi file with count
        for count_B,PDB_B in enumerate(tree_types["FileName"]):
            match = False

            #checks for n-glycan
            if csv["glycan_type"][count_A] != "n-glycan":
                continue
            
            #checks for matching PDB ID
            if PDB_A == PDB_B:
                #checks for matching TS chain ID
                if tree_types["TSChainId"][count_B] == csv["targetSugar_targetSugarChainID"][count_A]:
                    seqnum = tree_types["ID"][count_B]
                    split_seqnum = seqnum.split("/")
                    target_seqnum = csv["targetSugar_target_sugar_seqnum"][count_A]
                    sugar_index = csv["sugarIndex"][count_A]
                    Link_seqnum = target_seqnum - sugar_index
                    if split_seqnum[0] == f"NAG-{Link_seqnum}":
                        match = True
            
            if match != True:
                continue

            for x in from_tree_types:
                output[x].append(tree_types[x][count_B])
            
            for y,x in enumerate(from_XHpi):
                output[XHpi_rename[y]].append(csv[x][count_A])
            
            break


def process_data():
    match_search(hudson_csv,hudson_interactions)
    hudson_matches = pd.DataFrame(hudson_interactions)
    hudson_matches.to_csv("hudson_matches.csv")

    match_search(plevin_csv,plevin_interactions)
    plevin_matches = pd.DataFrame(plevin_interactions)
    plevin_matches.to_csv("plevin_matches.csv")


if __name__ == "__main__":
    process_data()
