import pandas as pd
import string

tree_types = pd.read_csv('glycan_tree_output.csv',low_memory=False)

New_tree_types = {"FileName":[],"TSChainId":[],"ID":[],"WURCS":[],"Results":[]}

alphabet = list(string.ascii_lowercase)
new_result = ""

def process_data(csv,output):
    for count,wurcs in enumerate(csv["WURCS"]):
        loop = True
        while loop == True:
            check_1 = False
            check_2 = False

            branch_check_1 = False
            branch_check_2 = False

            if csv["Results"][count] != "Unsuitable core glycan":
                break

            for letter in alphabet:
                if f"a4-b1_a6-{letter}1_b4-c1_c3-d1_c6-" in wurcs:
                    check_1 = True  

                if f"d2-{letter}1" in wurcs or f"d4-{letter}1" in wurcs:
                    branch_check_1 = True

                if f"b4-c1_c3-d1_c6-{letter}1" in wurcs:
                    check_2 = True
                    branch_2 = letter
                    for letter in alphabet:
                        if f"{branch_2}2-{letter}1" in wurcs or f"{branch_2}4-{letter}1" in wurcs:
                            branch_check_2 = True
            break
        
        if check_1 == True and check_2 == True:
            if branch_check_1 == True and branch_check_2 == True:
                new_result = "Complex"
            #closest thing to an xor 
            if branch_check_1 != branch_check_2:
                new_result = "Hybrid"
        else:
            new_result = csv["Results"][count]
        
        for key in output:
            if key == "Results":
                break
            output[key].append(csv[key][count])
        
        output["Results"].append(new_result)

if __name__ == "__main__":
    process_data(tree_types,New_tree_types)
    df = pd.DataFrame(New_tree_types)
    df.to_csv("tree_types_corrected.csv")
