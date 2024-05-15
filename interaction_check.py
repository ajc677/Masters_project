import pandas as pd

plevin_tree_types = pd.read_csv('plevin_matches.csv',low_memory=False)
hudson_tree_types = pd.read_csv('hudson_matches.csv',low_memory=False)

def check_total(tree_types):
    total_interactions = {"Complex":{},"Hybrid":{},"High Mannose":{},"Unsuitable core glycan":{}}
    #iterates through pdb ids in matches csv
    for count,pdb_id in enumerate(tree_types["FileName"]):        
        exists = False
        x = tree_types['Results'][count]

        for key in total_interactions[x]:
            if key == pdb_id:
                exists = True
            
        if exists == True:
            total_interactions[x][pdb_id] += 1
        
        else:
            total_interactions[x][pdb_id] = 1

    averages = {"Complex":"","Hybrid":"","High Mannose":"","Unsuitable core glycan":""}

    for key in total_interactions:
        g_type = key
        count = 0
        total = 0

        for key in total_interactions[g_type]:
            count += 1
            total += total_interactions[g_type][key]
        
        averages[g_type] = total
    
    print(averages)

def check_sugars():
 idk = ""
