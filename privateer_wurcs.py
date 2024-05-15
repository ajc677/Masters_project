# Extract WURCS code and sugar chain IDs for PDB files

import os
from privateer import privateer_core as pvt
import pandas as pd
import gzip
import shutil

output_csv_file_path = "WURCS_privateer_output.csv"

def get_sugar_id (totalWurcs_list, output_csv_file_path, file_name):
    ids = []
    wurcs_list = []
    
    for i in range(1, len(totalWurcs_list), 2):  # Start from the second line, skipping the first line
        ids.append(totalWurcs_list[i].strip())
        wurcs_list.append(totalWurcs_list[i + 1].strip())

    df = pd.DataFrame({"ID": ids, "WURCS": wurcs_list})
    df['TSChainId'] = df['ID'].apply(lambda x: x.split('_')[0][-1] if x.split('_')[0] else None)
    df['FileName'] = file_name
    df = df[['FileName', 'TSChainId', 'ID', 'WURCS']]
    df.to_csv(output_csv_file_path, mode='a', header=not os.path.exists(output_csv_file_path))


def get_wurcs (file_path, output_csv_file_path):
    x = os.path.splitext(os.path.basename(file_path))[0]
    file_name = x[3:7]
    totalWURCS = pvt.print_wurcs(file_path)
    totalWurcs_list = totalWURCS.splitlines()
    get_sugar_id(totalWurcs_list, output_csv_file_path, file_name)

if __name__ == "__main__":
    # List all files in the directory with a ".pdb" extension
    pdb_files = [x[3:7] for x in os.listdir("/vault/pdb_mirror/data/structures/all/pdb")]
    #pdb_files = ["8as0","3gzt"]
    for pdb_code in pdb_files:
        if not os.path.exists("/vault/privateer_database/pdb/"+ pdb_code[1:3] +"/"+ pdb_code +".json"):
            print("skip")
            continue

        gzipped_path =f"/vault/pdb_mirror/data/structures/all/pdb/pdb{pdb_code}.ent.gz"
        unzipped_path = f"/y/people/ajc677/Masters_project/pdb_tmp/pdb{pdb_code}.ent"
        with gzip.open(gzipped_path, 'rb') as f_in:
            with open(unzipped_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        try:
            get_wurcs(unzipped_path, output_csv_file_path)
        except:
            if os.path.isfile(unzipped_path):
                os.remove(unzipped_path)

        if os.path.isfile(unzipped_path):
            os.remove(unzipped_path)
