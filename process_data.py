import pandas as pd

def process_data():
    raw_hudson = pd.read_csv('combined_hudson.csv',low_memory=False)
    raw_plevin = pd.read_csv('combined_plevin.csv',low_memory=False)

    hudson_no_duplicates = raw_hudson.drop_duplicates(subset=["PDB", "sugarIndex", "glycanIndex", "targetSugar_targetSugarChainID", "targetSugar_target_sugar_type", "targetSugar_target_sugar_seqnum", "stackedResidue_stacked_residue_seqnum", "stackedResidue_stackedResidueChainID","stackedResidue_Trp_ring"])
    plevin_no_duplicates = raw_plevin.drop_duplicates(subset=["PDB", "sugarIndex", "glycanIndex", "targetSugar_targetSugarChainID", "targetSugar_target_sugar_type", "targetSugar_target_sugar_seqnum", "stackedResidue_stacked_residue_seqnum", "stackedResidue_stackedResidueChainID", "stackedResidue_Trp_ring"])

    hudson = hudson_no_duplicates.dropna(subset=['co_distance', 'hudson_theta_angle', 'hudson_cp_distance', 'plevin_theta_angle', 'plevin_phi_angle'])
    plevin = plevin_no_duplicates.dropna(subset=['co_distance', 'hudson_theta_angle', 'hudson_cp_distance', 'plevin_theta_angle', 'plevin_phi_angle'])

    hudson.to_csv("hudson_processed.csv")
    plevin.to_csv("plevin_processed.csv")

if __name__ == "__main__":
    process_data()
