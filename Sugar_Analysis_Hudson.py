import pandas as pd
ligand = {}
NGlycan = {}

with open("/y/people/ajc677/Masters_project/hudson_processed.csv") as fp:
    for line in fp:
        if line[:1] == ",":       #skips first line which begins with a comma
            continue
        
        line_list = []
        line_variable = ""
        for x in line:
            if x == ",":
                line_list.append(line_variable)
                line_variable = ""
            else:
                line_variable += x            
        if line_list[4] == "ligand":        #checks glycan type to work with
            glycan = ligand
        elif line_list[4] =="n-glycan":
            glycan = NGlycan
        else:
            continue
        
        sugar = line_list[11]
        
        check = False
        for key in glycan:            #checks if sugar has appeared
            if key == sugar:
                check = True

        if check == False:              #adds sugar to dict if not in already
            glycan[sugar] = []
            
        Values = {"CO_dist" : line_list[5],"Huds_theta" : line_list[6],"Huds_CP_dist" : line_list[7]}
        glycan[sugar].append(Values)
        
        
output = {"Glycan_type":[],"Sugar_Type":[],"Interaction_Count":[],"CO_dist_min":[],"CO_dist_max":[],"CO_dist_mean":[],"CO_dist_range":[],"Huds_theta_min":[],"Huds_theta_max":[],"Huds_theta_mean":[],"Huds_theta_range":[],"Huds_CP_dist_min":[],"Huds_CP_dist_max":[],"Huds_CP_dist_mean":[],"Huds_CP_dist_range":[]}

def analyse(glycan,type,output):
    for key in glycan:
        sugar = key
        Min_values = {"CO_dist" : 1000000.0,"Huds_theta" : 100000.0,"Huds_CP_dist" : 10000000.0}        #min values set to a higher value than expected
        Max_values = {"CO_dist" : 0.0,"Huds_theta" : 0.0,"Huds_CP_dist" : 0.0}              #max values set to a lower value than expected
        Mean = {"CO_dist" : "","Huds_theta" : "","Huds_CP_dist" : ""}
        Range = {"CO_dist" : "","Huds_theta" : "","Huds_CP_dist" : ""}
        Sum = {"CO_dist" : 0.0,"Huds_theta" : 0.0,"Huds_CP_dist" : 0.0}
        count = 0
        for x in glycan[key]:                                   
            for key in x:
                if float(x[key]) < float(Min_values[key]):
                    Min_values[key] = x[key]
                if float(x[key]) > float(Max_values[key]):
                    Max_values[key] = x[key]
                Sum[key] += float(x[key])
            count += 1
        for key in Mean:
            Mean[key] = Sum[key]/count
            Range[key] = float(Max_values[key]) - float(Min_values[key])

        new_output = {"Glycan_type": type,"Sugar_Type": sugar,"Interaction_Count": count,"CO_dist_min": Min_values["CO_dist"],"CO_dist_max": Max_values["CO_dist"],"CO_dist_mean": Mean["CO_dist"],"CO_dist_range": Range["CO_dist"],"Huds_theta_min":Min_values["Huds_theta"],"Huds_theta_max": Max_values["Huds_theta"],"Huds_theta_mean":Mean["Huds_theta"],"Huds_theta_range": Range["Huds_theta"],"Huds_CP_dist_min":Min_values["Huds_CP_dist"],"Huds_CP_dist_max": Max_values["Huds_CP_dist"],"Huds_CP_dist_mean":Mean["Huds_CP_dist"],"Huds_CP_dist_range": Range["Huds_CP_dist"]}
        for key in output:
            output[key].append(new_output[key])

type = "ligand"
analyse(ligand,type,output)

type = "N-Glycan"
analyse(NGlycan,type,output)

df = pd.DataFrame(output)

df.to_csv("Sugar_Analysis_Hudson.csv")
