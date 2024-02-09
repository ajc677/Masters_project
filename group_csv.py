import pandas as pd
import os 

def main(alg):
    to_combine_dir = "/y/people/ajc677/Masters_project/xhpi_run/%s_output" % alg

    master_df = pd.DataFrame()
    for path in os.scandir(to_combine_dir):
        df = pd.read_csv(path.path)

        master_df = pd.concat([master_df, df])
    
    master_df.to_csv("combined_%s.csv" % alg)


if __name__ == "__main__":
    main("plevin")
    main("hudson")
