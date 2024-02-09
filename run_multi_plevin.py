from multiprocessing import Pool 
from privateer import privateer_core as pvtcore
import pandas as pd
import os
from tqdm import tqdm 
import sys
import gzip
import shutil

# def mute():
#   sys.stdout = open(os.devnull, 'w')

def worker(pdb_code):
    # print(pdb_code)
    hydrogenated_pdb_path = f"/vault/pdb_hydrogenated/hydrogenated_pdb{pdb_code}.pdb"
    gzipped_path =f"/vault/pdb_mirror/data/structures/all/pdb/pdb{pdb_code}.ent.gz"
    unzipped_path = f"/vault/test/pdb{pdb_code}.ent"
    with gzip.open(gzipped_path, 'rb') as f_in:
        with open(unzipped_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    try:
        interactions = pvtcore.GlycosylationInteractions(
            path_to_model_file=unzipped_path,
            path_to_output_file=hydrogenated_pdb_path,
            enableHBonds=True, 
            chpi_algorithm="plevin" )

        interactions_summary=interactions.get_all_detected_interactions()
    except: 
    
        return None
    
    if os.path.isfile(unzipped_path):
        os.remove(unzipped_path)

    chpi_detected = False 
    output_df = pd.DataFrame()
    for d in interactions_summary:
        if d["CH_Pi"]: 
            for chpi in d["CH_Pi"]:
                df = pd.json_normalize(d['CH_Pi'], sep='_')
                df["glycanIndex"] = d["glycanIndex"]
                df["totalGlycansInModel"] = d["totalGlycansInModel"]
                df["PDB"] = pdb_code
                output_df = pd.concat([output_df, df])
                chpi_detected = True
    
    if chpi_detected:
        dictionary = output_df.to_dict('records')
        output_df.to_csv(f"xhpi_run/plevin_output/{pdb_code}.csv", index=False)
        # for x in dictionary:
        #     print(x)
        return dictionary
    return None

def get_pdb_list(): 
    return [x[3:7] for x in os.listdir("/vault/pdb_mirror/data/structures/all/pdb")]

def run_multithreaded_job():

    pdb_list = get_pdb_list()
    #pdb_list = ["5fjj", "5fji"]
    output_list = [] 

    with Pool() as pool_:
        result = list(tqdm(pool_.imap_unordered(worker, pdb_list), total=len(pdb_list))) 
        if result:
            for x in result:
                output_list.extend(x)

    output_df = pd.DataFrame(output_list)

    output_df.to_csv("xhpi_run/plevin_output.csv", index=False)
    
if __name__ == "__main__":
    run_multithreaded_job()
