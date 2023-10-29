from run import run_proposed, heuristic2, heuristic3, heuristic4, heuristic5, heuristic6
import csv
import time
import json
if __name__ == '__main__':
    path_nsf = [r'./data_1_9/nsf_centers_easy_s1.json', r'./data_1_9/nsf_centers_easy_s2.json',r'./data_1_9/nsf_centers_easy_s3.json', r'./data_1_9/nsf_centers_hard_s1.json', r'./data_1_9/nsf_centers_hard_s2.json',r'./data_1_9/nsf_centers_hard_s3.json', r'./data_1_9/nsf_centers_normal_s1.json',r'./data_1_9/nsf_centers_normal_s2.json', r'./data_1_9/nsf_centers_normal_s3.json',r'./data_1_9/nsf_rural_easy_s1.json', r'./data_1_9/nsf_rural_easy_s2.json', r'./data_1_9/nsf_rural_easy_s3.json', r'./data_1_9/nsf_rural_hard_s1.json', r'./data_1_9/nsf_rural_hard_s2.json', r'./data_1_9/nsf_rural_hard_s3.json', r'./data_1_9/nsf_rural_normal_s1.json', r'./data_1_9/nsf_rural_normal_s2.json', r'./data_1_9/nsf_rural_normal_s3.json', r'./data_1_9/nsf_uniform_easy_s1.json', r'./data_1_9/nsf_uniform_easy_s2.json', r'./data_1_9/nsf_uniform_easy_s3.json', r'./data_1_9/nsf_uniform_hard_s1.json', r'./data_1_9/nsf_uniform_hard_s2.json', r'./data_1_9/nsf_uniform_hard_s3.json', r'./data_1_9/nsf_uniform_normal_s1.json', r'./data_1_9/nsf_uniform_normal_s2.json', r'./data_1_9/nsf_uniform_normal_s3.json', r'./data_1_9/nsf_urban_easy_s1.json', r'./data_1_9/nsf_urban_easy_s2.json', r'./data_1_9/nsf_urban_easy_s3.json', r'./data_1_9/nsf_urban_hard_s1.json', r'./data_1_9/nsf_urban_hard_s2.json', r'./data_1_9/nsf_urban_hard_s3.json',r'./data_1_9/nsf_urban_normal_s1.json', r'./data_1_9/nsf_urban_normal_s2.json', r'./data_1_9/nsf_urban_normal_s3.json']
    for path in path_nsf:
        print(path)
        result = {}
        result["dataset"] = path
        fitness2, reject2, cost2,  proc2 = heuristic2(path, 0.5, 10)
        result["heuristic2"] = fitness2
        fitness3, reject3, cost3, proc3 = heuristic3(path, 0.5, 10)
        result["heuristic3"] = fitness3
        fitness4, reject4, cost4, proc4 = heuristic4(path, 0.5, 10)
        result["heuristic4"] = fitness4
        fitness5, reject5, cost5, proc5 = heuristic5(path, 0.5, 10)
        result["heuristic5"] = fitness5
        fitness6, reject6, cost6, proc6 = heuristic6(path, 0.5, 10)
        result["heuristic6"] = fitness6
        
        pathname = "./Heuristic/" + path[11:-5] + ".csv"
        with open(pathname, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dataset", "heuristic2", "heuristic3", "heuristic4", "heuristic5", "heuristic6"])
            writer.writerow([path[11:-5],fitness2, fitness3, fitness4, fitness5, fitness6])
    
    path_conus = [r'./data_1_9/conus_centers_easy_s1.json', r'./data_1_9/conus_centers_easy_s2.json',r'./data_1_9/conus_centers_easy_s3.json', r'./data_1_9/conus_centers_hard_s1.json', r'./data_1_9/conus_centers_hard_s2.json',r'./data_1_9/conus_centers_hard_s3.json', r'./data_1_9/conus_centers_normal_s1.json',r'./data_1_9/conus_centers_normal_s2.json', r'./data_1_9/conus_centers_normal_s3.json',r'./data_1_9/conus_rural_easy_s1.json', r'./data_1_9/conus_rural_easy_s2.json', r'./data_1_9/conus_rural_easy_s3.json', r'./data_1_9/conus_rural_hard_s1.json', r'./data_1_9/conus_rural_hard_s2.json', r'./data_1_9/conus_rural_hard_s3.json', r'./data_1_9/conus_rural_normal_s1.json', r'./data_1_9/conus_rural_normal_s2.json', r'./data_1_9/conus_rural_normal_s3.json', r'./data_1_9/conus_uniform_easy_s1.json', r'./data_1_9/conus_uniform_easy_s2.json', r'./data_1_9/conus_uniform_easy_s3.json', r'./data_1_9/conus_uniform_hard_s1.json', r'./data_1_9/conus_uniform_hard_s2.json', r'./data_1_9/conus_uniform_hard_s3.json', r'./data_1_9/conus_uniform_normal_s1.json', r'./data_1_9/conus_uniform_normal_s2.json', r'./data_1_9/conus_uniform_normal_s3.json', r'./data_1_9/conus_urban_easy_s1.json', r'./data_1_9/conus_urban_easy_s2.json', r'./data_1_9/conus_urban_easy_s3.json', r'./data_1_9/conus_urban_hard_s1.json', r'./data_1_9/conus_urban_hard_s2.json', r'./data_1_9/conus_urban_hard_s3.json',r'./data_1_9/conus_urban_normal_s1.json', r'./data_1_9/conus_urban_normal_s2.json', r'./data_1_9/conus_urban_normal_s3.json']
    for path in path_conus:
        print(path)
        result = {}
        result["dataset"] = path
        fitness2, reject2, cost2,  proc2 = heuristic2(path, 0.5, 10)
        result["heuristic2"] = fitness2
        fitness3, reject3, cost3, proc3 = heuristic3(path, 0.5, 10)
        result["heuristic3"] = fitness3
        fitness4, reject4, cost4, proc4 = heuristic4(path, 0.5, 10)
        result["heuristic4"] = fitness4
        fitness5, reject5, cost5, proc5 = heuristic5(path, 0.5, 10)
        result["heuristic5"] = fitness5
        fitness6, reject6, cost6, proc6 = heuristic6(path, 0.5, 10)
        result["heuristic6"] = fitness6
        
        pathname = "./Heuristic/" + path[11:-5] + ".csv"
        with open(pathname, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dataset", "heuristic2", "heuristic3", "heuristic4", "heuristic5", "heuristic6"])
            writer.writerow([path[11:-5],fitness2, fitness3, fitness4, fitness5, fitness6])

    path_cogent = [r'./data_1_9/cogent_centers_easy_s1.json', r'./data_1_9/cogent_centers_easy_s2.json',r'./data_1_9/cogent_centers_easy_s3.json', r'./data_1_9/cogent_centers_hard_s1.json', r'./data_1_9/cogent_centers_hard_s2.json',r'./data_1_9/cogent_centers_hard_s3.json', r'./data_1_9/cogent_centers_normal_s1.json',r'./data_1_9/cogent_centers_normal_s2.json', r'./data_1_9/cogent_centers_normal_s3.json',r'./data_1_9/cogent_rural_easy_s1.json', r'./data_1_9/cogent_rural_easy_s2.json', r'./data_1_9/cogent_rural_easy_s3.json', r'./data_1_9/cogent_rural_hard_s1.json', r'./data_1_9/cogent_rural_hard_s2.json', r'./data_1_9/cogent_rural_hard_s3.json', r'./data_1_9/cogent_rural_normal_s1.json', r'./data_1_9/cogent_rural_normal_s2.json', r'./data_1_9/cogent_rural_normal_s3.json', r'./data_1_9/cogent_uniform_easy_s1.json', r'./data_1_9/cogent_uniform_easy_s2.json', r'./data_1_9/cogent_uniform_easy_s3.json', r'./data_1_9/cogent_uniform_hard_s1.json', r'./data_1_9/cogent_uniform_hard_s2.json', r'./data_1_9/cogent_uniform_hard_s3.json', r'./data_1_9/cogent_uniform_normal_s1.json', r'./data_1_9/cogent_uniform_normal_s2.json', r'./data_1_9/cogent_uniform_normal_s3.json', r'./data_1_9/cogent_urban_easy_s1.json', r'./data_1_9/cogent_urban_easy_s2.json', r'./data_1_9/cogent_urban_easy_s3.json', r'./data_1_9/cogent_urban_hard_s1.json', r'./data_1_9/cogent_urban_hard_s2.json', r'./data_1_9/cogent_urban_hard_s3.json',r'./data_1_9/cogent_urban_normal_s1.json', r'./data_1_9/cogent_urban_normal_s2.json', r'./data_1_9/cogent_urban_normal_s3.json']
    for path in path_cogent:
        print(path)
        result = {}
        result["dataset"] = path
        fitness2, reject2, cost2,  proc2 = heuristic2(path, 0.5, 10)
        result["heuristic2"] = fitness2
        fitness3, reject3, cost3, proc3 = heuristic3(path, 0.5, 10)
        result["heuristic3"] = fitness3
        fitness4, reject4, cost4, proc4 = heuristic4(path, 0.5, 10)
        result["heuristic4"] = fitness4
        fitness5, reject5, cost5, proc5 = heuristic5(path, 0.5, 10)
        result["heuristic5"] = fitness5
        fitness6, reject6, cost6, proc6 = heuristic6(path, 0.5, 10)
        result["heuristic6"] = fitness6
        
        pathname = "./Heuristic/" + path[11:-5] + ".csv"
        with open(pathname, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dataset", "heuristic2", "heuristic3", "heuristic4", "heuristic5", "heuristic6"])
            writer.writerow([path[11:-5],fitness2, fitness3, fitness4, fitness5, fitness6])