import json
import os
import pandas as pd


count = {}

for folder in os.listdir("/vault/privateer_database/pdb"):
      for file in os.listdir("/vault/privateer_database/pdb/" + folder):                
        with open('/vault/privateer_database/pdb/' + folder + '/' + file ,'r') as pdb_file:
            data = json.load(pdb_file)
            
            for glycan_type in data["glycans"]:
                for count_glycans,glycan_data in enumerate(data["glycans"][glycan_type]):
                    for count_sugars,sugar_data in enumerate(data["glycans"][glycan_type][count_glycans]["sugars"]):
                        sugarId = data["glycans"][glycan_type][count_glycans]["sugars"][count_sugars]["sugarId"]
                        sugarId_cropped = sugarId.partition("-")[0]
                        
                        check = False
                        for key in count:            #checks if sugar has appeared
                            if key == sugarId_cropped:
                                check = True

                        if check == True:
                            count[sugarId_cropped] += 1

                        else:              #adds sugar to dict if not in already
                            count[sugarId_cropped] = 0

for key in count:
    count[key] = [count[key]]

df = pd.DataFrame(count)

df.to_csv("Sugar_count.csv")
