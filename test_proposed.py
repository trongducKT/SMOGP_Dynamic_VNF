from run import run_proposed
import csv
import time
import json
if __name__ == '__main__':
    path_nsf = [r'./data_1_9/nsf_centers_easy_s1.json', r'./data_1_9/nsf_centers_easy_s2.json',r'./data_1_9/nsf_centers_easy_s3.json', r'./data_1_9/nsf_centers_hard_s1.json', r'./data_1_9/nsf_centers_hard_s2.json',r'./data_1_9/nsf_centers_hard_s3.json', r'./data_1_9/nsf_centers_normal_s1.json',r'./data_1_9/nsf_centers_normal_s2.json', r'./data_1_9/nsf_centers_normal_s3.json',r'./data_1_9/nsf_rural_easy_s1.json', r'./data_1_9/nsf_rural_easy_s2.json', r'./data_1_9/nsf_rural_easy_s3.json', r'./data_1_9/nsf_rural_hard_s1.json', r'./data_1_9/nsf_rural_hard_s2.json', r'./data_1_9/nsf_rural_hard_s3.json', r'./data_1_9/nsf_rural_normal_s1.json', r'./data_1_9/nsf_rural_normal_s2.json', r'./data_1_9/nsf_rural_normal_s3.json', r'./data_1_9/nsf_uniform_easy_s1.json', r'./data_1_9/nsf_uniform_easy_s2.json', r'./data_1_9/nsf_uniform_easy_s3.json', r'./data_1_9/nsf_uniform_hard_s1.json', r'./data_1_9/nsf_uniform_hard_s2.json', r'./data_1_9/nsf_uniform_hard_s3.json', r'./data_1_9/nsf_uniform_normal_s1.json', r'./data_1_9/nsf_uniform_normal_s2.json', r'./data_1_9/nsf_uniform_normal_s3.json', r'./data_1_9/nsf_urban_easy_s1.json', r'./data_1_9/nsf_urban_easy_s2.json', r'./data_1_9/nsf_urban_easy_s3.json', r'./data_1_9/nsf_urban_hard_s1.json', r'./data_1_9/nsf_urban_hard_s2.json', r'./data_1_9/nsf_urban_hard_s3.json',r'./data_1_9/nsf_urban_normal_s1.json', r'./data_1_9/nsf_urban_normal_s2.json', r'./data_1_9/nsf_urban_normal_s3.json']
    for path in path_nsf:
        print(path)
        result = {}
        result["dataset"] = path
        fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, 96, 0.5, 10, 100,2,8,8,1000,100,0.8,0.1)
        print("GP", fitness, rejected, cost)

        result["fitness"] = fitness
        result["rejected"] = rejected
        result["cost"] = cost
        result["fitness_train"] = fitness_train
        result["time_train"] = time_train
        
        pathname = "./Result_summary/Proposed/" + path[11:-5] + ".csv"
        with open(pathname, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dataset", "fitness", "rejected", "cost", "fitness_train", "time_train"])
            writer.writerow([path[11:-5],fitness, rejected, cost, fitness_train, time_train])
        
        pathname_history = "./Result_summary/Proposed/Convergence_" + path[11:-5] + ".json"
        with open(pathname_history,'w') as file:
            json.dump(fitness_history, file)
    
    path_conus = [r'./data_1_9/conus_centers_easy_s1.json', r'./data_1_9/conus_centers_easy_s2.json',r'./data_1_9/conus_centers_easy_s3.json', r'./data_1_9/conus_centers_hard_s1.json', r'./data_1_9/conus_centers_hard_s2.json',r'./data_1_9/conus_centers_hard_s3.json', r'./data_1_9/conus_centers_normal_s1.json',r'./data_1_9/conus_centers_normal_s2.json', r'./data_1_9/conus_centers_normal_s3.json',r'./data_1_9/conus_rural_easy_s1.json', r'./data_1_9/conus_rural_easy_s2.json', r'./data_1_9/conus_rural_easy_s3.json', r'./data_1_9/conus_rural_hard_s1.json', r'./data_1_9/conus_rural_hard_s2.json', r'./data_1_9/conus_rural_hard_s3.json', r'./data_1_9/conus_rural_normal_s1.json', r'./data_1_9/conus_rural_normal_s2.json', r'./data_1_9/conus_rural_normal_s3.json', r'./data_1_9/conus_uniform_easy_s1.json', r'./data_1_9/conus_uniform_easy_s2.json', r'./data_1_9/conus_uniform_easy_s3.json', r'./data_1_9/conus_uniform_hard_s1.json', r'./data_1_9/conus_uniform_hard_s2.json', r'./data_1_9/conus_uniform_hard_s3.json', r'./data_1_9/conus_uniform_normal_s1.json', r'./data_1_9/conus_uniform_normal_s2.json', r'./data_1_9/conus_uniform_normal_s3.json', r'./data_1_9/conus_urban_easy_s1.json', r'./data_1_9/conus_urban_easy_s2.json', r'./data_1_9/conus_urban_easy_s3.json', r'./data_1_9/conus_urban_hard_s1.json', r'./data_1_9/conus_urban_hard_s2.json', r'./data_1_9/conus_urban_hard_s3.json',r'./data_1_9/conus_urban_normal_s1.json', r'./data_1_9/conus_urban_normal_s2.json', r'./data_1_9/conus_urban_normal_s3.json']
    for path in path_conus:
            print(path)
            result = {}
            result["dataset"] = path
            fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, 96, 0.5, 10, 45,2,8,8,1000,100,0.8,0.1)
            print("GP", fitness, rejected, cost)

            result["fitness"] = fitness
            result["rejected"] = rejected
            result["cost"] = cost
            result["fitness_train"] = fitness_train
            result["time_train"] = time_train
            
            pathname = "./Result_summary/Proposed/" + path[11:-5] + ".csv"
            with open(pathname, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["dataset", "fitness", "rejected", "cost", "fitness_train", "time_train"])
                writer.writerow([path[11:-5],fitness, rejected, cost, fitness_train, time_train])
            
            pathname_history = "./Result_summary/Proposed/Convergence_" + path[11:-5] + ".json"
            with open(pathname_history,'w') as file:
                json.dump(fitness_history, file)

    path_conus = [r'./data_1_9/cogent_centers_easy_s1.json', r'./data_1_9/cogent_centers_easy_s2.json',r'./data_1_9/cogent_centers_easy_s3.json', r'./data_1_9/cogent_centers_hard_s1.json', r'./data_1_9/cogent_centers_hard_s2.json',r'./data_1_9/cogent_centers_hard_s3.json', r'./data_1_9/cogent_centers_normal_s1.json',r'./data_1_9/cogent_centers_normal_s2.json', r'./data_1_9/cogent_centers_normal_s3.json',r'./data_1_9/cogent_rural_easy_s1.json', r'./data_1_9/cogent_rural_easy_s2.json', r'./data_1_9/cogent_rural_easy_s3.json', r'./data_1_9/cogent_rural_hard_s1.json', r'./data_1_9/cogent_rural_hard_s2.json', r'./data_1_9/cogent_rural_hard_s3.json', r'./data_1_9/cogent_rural_normal_s1.json', r'./data_1_9/cogent_rural_normal_s2.json', r'./data_1_9/cogent_rural_normal_s3.json', r'./data_1_9/cogent_uniform_easy_s1.json', r'./data_1_9/cogent_uniform_easy_s2.json', r'./data_1_9/cogent_uniform_easy_s3.json', r'./data_1_9/cogent_uniform_hard_s1.json', r'./data_1_9/cogent_uniform_hard_s2.json', r'./data_1_9/cogent_uniform_hard_s3.json', r'./data_1_9/cogent_uniform_normal_s1.json', r'./data_1_9/cogent_uniform_normal_s2.json', r'./data_1_9/cogent_uniform_normal_s3.json', r'./data_1_9/cogent_urban_easy_s1.json', r'./data_1_9/cogent_urban_easy_s2.json', r'./data_1_9/cogent_urban_easy_s3.json', r'./data_1_9/cogent_urban_hard_s1.json', r'./data_1_9/cogent_urban_hard_s2.json', r'./data_1_9/cogent_urban_hard_s3.json',r'./data_1_9/cogent_urban_normal_s1.json', r'./data_1_9/cogent_urban_normal_s2.json', r'./data_1_9/cogent_urban_normal_s3.json']
    for path in path_conus:
        print(path)
        result = {}
        result["dataset"] = path
        fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, 96, 0.5, 10, 45,2,8,8,1000,100,0.8,0.1)
        print("GP", fitness, rejected, cost)

        result["fitness"] = fitness
        result["rejected"] = rejected
        result["cost"] = cost
        result["fitness_train"] = fitness_train
        result["time_train"] = time_train
        
        pathname = "./Result_summary/Proposed/" + path[11:-5] + ".csv"
        with open(pathname, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["dataset", "fitness", "rejected", "cost", "fitness_train", "time_train"])
            writer.writerow([path[11:-5],fitness, rejected, cost, fitness_train, time_train])
        
        pathname_history = "./Result_summary/Proposed/Convergence_" + path[11:-5] + ".json"
        with open(pathname_history,'w') as file:
            json.dump(fitness_history, file)
    