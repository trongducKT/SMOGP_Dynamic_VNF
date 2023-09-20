from run import run_proposed, heuristic2, heuristic3, heuristic1
import csv

if __name__ == '__main__':



    path_conus=[r'./data_1_9/conus_centers_easy_s1.json', r'./data_1_9/conus_centers_easy_s2.json', r'./data_1_9/conus_centers_easy_s3.json', r'./data_1_9/conus_centers_hard_s1.json', r'./data_1_9/conus_centers_hard_s2.json', r'./data_1_9/conus_centers_hard_s3.json',r'./data_1_9/conus_centers_normal_s1.json',r'./data_1_9/conus_centers_normal_s2.json', r'./data_1_9/conus_centers_normal_s3.json',r'./data_1_9/conus_rural_easy_s1.json', r'./data_1_9/conus_rural_easy_s2.json', r'./data_1_9/conus_rural_easy_s3.json', r'./data_1_9/conus_rural_hard_s1.json', r'./data_1_9/conus_rural_hard_s2.json', r'./data_1_9/conus_rural_hard_s3.json', r'./data_1_9/conus_rural_normal_s1.json', r'./data_1_9/conus_rural_normal_s2.json', r'./data_1_9/conus_rural_normal_s3.json', r'./data_1_9/conus_uniform_easy_s1.json', r'./data_1_9/conus_uniform_easy_s2.json', r'./data_1_9/conus_uniform_easy_s3.json', r'./data_1_9/conus_uniform_hard_s1.json', r'./data_1_9/conus_uniform_hard_s2.json', r'./data_1_9/conus_uniform_hard_s3.json', r'./data_1_9/conus_uniform_normal_s1.json', r'./data_1_9/conus_uniform_normal_s2.json', r'./data_1_9/conus_uniform_normal_s3.json', r'./data_1_9/conus_urban_easy_s1.json', r'./data_1_9/conus_urban_easy_s2.json', r'./data_1_9/conus_urban_easy_s3.json', r'./data_1_9/conus_urban_hard_s1.json', r'./data_1_9/conus_urban_hard_s2.json', r'./data_1_9/conus_urban_hard_s3.json',r'./data_1_9/conus_urban_normal_s1.json', r'./data_1_9/conus_urban_normal_s2.json', r'./data_1_9/conus_urban_normal_s3.json' ]
    for path in path_conus:
        print(path)
        result = {}
        result["dataset"] = path
        fitness, rejected, cost, proc, sum_gen= run_proposed(path, 100, 0.5, 5, 45, 2, 8, 4, 10, 100, 0.8, 0.1 )
        #print(fitness, rejected, cost)

        fitness1, rejected1, cost1, proc1= heuristic1(path, 0.5, 5)

        fitness2, rejected2, cost2, proc2 = heuristic2(path, 0.5, 5)

        fitness3, rejected3, cost3, proc3 = heuristic3(path, 0.5, 5)

        result["proposed_fitness"] = fitness
        result["proposed_rejected"] = rejected
        result["proposed_cost"] = cost
        result["h1_fitness"] = fitness1
        result["h1_rejected"] = rejected1
        result["h1_cost"] = cost1
        result["h2_fitness"] = fitness2
        result["h2_rejected"] = rejected2
        result["h2_cost"] = cost2
        result["h3_fitness"] = fitness3
        result["h3_rejected"] = rejected3
        result["h3_cost"] = cost3
        print(fitness, rejected, cost)
        print(fitness1, rejected1, cost1)
        print(fitness2, rejected2, cost2)
        print(fitness3, rejected3, cost3)
        with open (r"./result/result1_9_17_9.csv", "a") as f:
            fieldnames = ['dataset', 'proposed_fitness', 'proposed_rejected', 'proposed_cost', 'h1_fitness', 'h1_rejected', 'h1_cost', 'h2_fitness', 'h2_rejected', 'h2_cost', 'h3_fitness', 'h3_rejected', 'h3_cost']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(result)
            
        gen = {}
        gen["dataset"] = path
        gen["gen"] = sum_gen
        with open (r"./result/result1_9_17_9_generation.csv", "a") as f:
            fieldnames = ['dataset', 'gen']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(gen)
        
    
    

