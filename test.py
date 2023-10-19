from run import run_proposed, heuristic2, heuristic3, heuristic1, heuristic5, heuristic6
import csv
import time
if __name__ == '__main__':
    path_nsf=path_nsf = [r'./data_1_9/nsf_centers_easy_s1.json', r'./data_1_9/nsf_centers_easy_s2.json',r'./data_1_9/nsf_centers_easy_s3.json', r'./data_1_9/nsf_centers_hard_s1.json', r'./data_1_9/nsf_centers_hard_s2.json',r'./data_1_9/nsf_centers_hard_s3.json', r'./data_1_9/nsf_centers_normal_s1.json',r'./data_1_9/nsf_centers_normal_s2.json', r'./data_1_9/nsf_centers_normal_s3.json',r'./data_1_9/nsf_rural_easy_s1.json', r'./data_1_9/nsf_rural_easy_s2.json', r'./data_1_9/nsf_rural_easy_s3.json', r'./data_1_9/nsf_rural_hard_s1.json', r'./data_1_9/nsf_rural_hard_s2.json', r'./data_1_9/nsf_rural_hard_s3.json', r'./data_1_9/nsf_rural_normal_s1.json', r'./data_1_9/nsf_rural_normal_s2.json', r'./data_1_9/nsf_rural_normal_s3.json', r'./data_1_9/nsf_uniform_easy_s1.json', r'./data_1_9/nsf_uniform_easy_s2.json', r'./data_1_9/nsf_uniform_easy_s3.json', r'./data_1_9/nsf_uniform_hard_s1.json', r'./data_1_9/nsf_uniform_hard_s2.json', r'./data_1_9/nsf_uniform_hard_s3.json', r'./data_1_9/nsf_uniform_normal_s1.json', r'./data_1_9/nsf_uniform_normal_s2.json', r'./data_1_9/nsf_uniform_normal_s3.json', r'./data_1_9/nsf_urban_easy_s1.json', r'./data_1_9/nsf_urban_easy_s2.json', r'./data_1_9/nsf_urban_easy_s3.json', r'./data_1_9/nsf_urban_hard_s1.json', r'./data_1_9/nsf_urban_hard_s2.json', r'./data_1_9/nsf_urban_hard_s3.json',r'./data_1_9/nsf_urban_normal_s1.json', r'./data_1_9/nsf_urban_normal_s2.json', r'./data_1_9/nsf_urban_normal_s3.json']
#     path_nsf = [r'./data_1_9/nsf_urban_hard_s3.json']
    for path in path_nsf:
        print(path)
        result = {}
        result["dataset"] = path
        fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, 4, 0.5, 10, 10, 2, 8, 4, 10, 100, 0.8, 0.5 )
        print("GP", fitness, rejected, cost)

#         fitness1, rejected1, cost1, proc1= heuristic1(path, 0.5, 10)

        fitness5, rejected5, cost5, proc5 = heuristic5(path, 0.5, 10)

        fitness6, rejected6, cost6, proc6 = heuristic6(path, 0.5, 10)
#         print("FIFO", fitness2, rejected2, cost2)
#         print("DD", fitness3, rejected3, cost3)
#         time.sleep(20)
#         result["proposed_fitness"] = fitness
#         result["proposed_rejected"] = rejected
#         result["proposed_cost"] = cost
        result["h5_fitness"] = fitness5
        result["h5_rejected"] = rejected5
        result["h5_cost"] = cost5
        result["h6_fitness"] = fitness6
        result["h6_rejected"] = rejected6
        result["h6_cost"] = cost6
#         print(fitness, rejected, cost)
#         print(fitness1, rejected1, cost1)
#         print(fitness2, rejected2, cost2)
#         print(fitness3, rejected3, cost3)
        with open (r"./result/result1_9_9_10.csv", "a") as f:
            fieldnames = ['dataset', 'h5_fitness', 'h5_rejected', 'h5_cost', 'h6_fitness', 'h6_rejected', 'h6_cost']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(result)
            
            
    path_nsf=path_nsf = [r'./data_1_9/conus_centers_easy_s1.json', r'./data_1_9/conus_centers_easy_s2.json',r'./data_1_9/conus_centers_easy_s3.json', r'./data_1_9/conus_centers_hard_s1.json', r'./data_1_9/conus_centers_hard_s2.json',r'./data_1_9/conus_centers_hard_s3.json', r'./data_1_9/conus_centers_normal_s1.json',r'./data_1_9/conus_centers_normal_s2.json', r'./data_1_9/conus_centers_normal_s3.json',r'./data_1_9/conus_rural_easy_s1.json', r'./data_1_9/conus_rural_easy_s2.json', r'./data_1_9/conus_rural_easy_s3.json', r'./data_1_9/conus_rural_hard_s1.json', r'./data_1_9/conus_rural_hard_s2.json', r'./data_1_9/conus_rural_hard_s3.json', r'./data_1_9/conus_rural_normal_s1.json', r'./data_1_9/conus_rural_normal_s2.json', r'./data_1_9/conus_rural_normal_s3.json', r'./data_1_9/conus_uniform_easy_s1.json', r'./data_1_9/conus_uniform_easy_s2.json', r'./data_1_9/conus_uniform_easy_s3.json', r'./data_1_9/conus_uniform_hard_s1.json', r'./data_1_9/conus_uniform_hard_s2.json', r'./data_1_9/conus_uniform_hard_s3.json', r'./data_1_9/conus_uniform_normal_s1.json', r'./data_1_9/conus_uniform_normal_s2.json', r'./data_1_9/conus_uniform_normal_s3.json', r'./data_1_9/conus_urban_easy_s1.json', r'./data_1_9/conus_urban_easy_s2.json', r'./data_1_9/conus_urban_easy_s3.json', r'./data_1_9/conus_urban_hard_s1.json', r'./data_1_9/conus_urban_hard_s2.json', r'./data_1_9/conus_urban_hard_s3.json',r'./data_1_9/conus_urban_normal_s1.json', r'./data_1_9/conus_urban_normal_s2.json', r'./data_1_9/conus_urban_normal_s3.json']
#     path_nsf = [r'./data_1_9/nsf_urban_hard_s3.json']
    for path in path_nsf:
        print(path)
        result = {}
        result["dataset"] = path
#         fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, 100, 0.5, 10, 20, 2, 8, 4, 10, 100, 0.8, 0.5 )
#         print("GP", fitness, rejected, cost)

#         fitness1, rejected1, cost1, proc1= heuristic1(path, 0.5, 10)

        fitness5, rejected5, cost5, proc5 = heuristic5(path, 0.5, 5)

        fitness6, rejected6, cost6, proc6 = heuristic6(path, 0.5, 5)
#         print("FIFO", fitness2, rejected2, cost2)
#         print("DD", fitness3, rejected3, cost3)
#         time.sleep(20)
#         result["proposed_fitness"] = fitness
#         result["proposed_rejected"] = rejected
#         result["proposed_cost"] = cost
        result["h5_fitness"] = fitness5
        result["h5_rejected"] = rejected5
        result["h5_cost"] = cost5
        result["h6_fitness"] = fitness6
        result["h6_rejected"] = rejected6
        result["h6_cost"] = cost6
#         print(fitness, rejected, cost)
#         print(fitness1, rejected1, cost1)
#         print(fitness2, rejected2, cost2)
#         print(fitness3, rejected3, cost3)
        with open (r"./result/result1_9_9_10.csv", "a") as f:
            fieldnames = ['dataset', 'h5_fitness', 'h5_rejected', 'h5_cost', 'h6_fitness', 'h6_rejected', 'h6_cost']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(result)

            
    path_nsf=path_nsf = [r'./input_25/cogent_centers_easy_s1.json', r'./input_25/cogent_centers_easy_s2.json',r'./input_25/cogent_centers_easy_s3.json', r'./input_25/cogent_centers_hard_s1.json', r'./input_25/cogent_centers_hard_s2.json',r'./input_25/cogent_centers_hard_s3.json', r'./input_25/cogent_centers_normal_s1.json',r'./input_25/cogent_centers_normal_s2.json', r'./input_25/cogent_centers_normal_s3.json',r'./input_25/cogent_rural_easy_s1.json', r'./input_25/cogent_rural_easy_s2.json', r'./input_25/cogent_rural_easy_s3.json', r'./input_25/cogent_rural_hard_s1.json', r'./input_25/cogent_rural_hard_s2.json', r'./input_25/cogent_rural_hard_s3.json', r'./input_25/cogent_rural_normal_s1.json', r'./input_25/cogent_rural_normal_s2.json', r'./input_25/cogent_rural_normal_s3.json', r'./input_25/cogent_uniform_easy_s1.json', r'./input_25/cogent_uniform_easy_s2.json', r'./input_25/cogent_uniform_easy_s3.json', r'./input_25/cogent_uniform_hard_s1.json', r'./input_25/cogent_uniform_hard_s2.json', r'./input_25/cogent_uniform_hard_s3.json', r'./input_25/cogent_uniform_normal_s1.json', r'./input_25/cogent_uniform_normal_s2.json', r'./input_25/cogent_uniform_normal_s3.json', r'./input_25/cogent_urban_easy_s1.json', r'./input_25/cogent_urban_easy_s2.json', r'./input_25/cogent_urban_easy_s3.json', r'./input_25/cogent_urban_hard_s1.json', r'./input_25/cogent_urban_hard_s2.json', r'./input_25/cogent_urban_hard_s3.json',r'./input_25/cogent_urban_normal_s1.json', r'./input_25/cogent_urban_normal_s2.json', r'./input_25/cogent_urban_normal_s3.json']
#     path_nsf = [r'./data_1_9/nsf_urban_hard_s3.json']
    for path in path_nsf:
        print(path)
        result = {}
        result["dataset"] = path
#         fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, 100, 0.5, 10, 20, 2, 8, 4, 10, 100, 0.8, 0.5 )
#         print("GP", fitness, rejected, cost)

#         fitness1, rejected1, cost1, proc1= heuristic1(path, 0.5, 10)

        fitness5, rejected5, cost5, proc5 = heuristic5(path, 0.5, 5)

        fitness6, rejected6, cost6, proc6 = heuristic6(path, 0.5, 5)
#         print("FIFO", fitness2, rejected2, cost2)
#         print("DD", fitness3, rejected3, cost3)
#         time.sleep(20)
#         result["proposed_fitness"] = fitness
#         result["proposed_rejected"] = rejected
#         result["proposed_cost"] = cost
        result["h5_fitness"] = fitness5
        result["h5_rejected"] = rejected5
        result["h5_cost"] = cost5
        result["h6_fitness"] = fitness6
        result["h6_rejected"] = rejected6
        result["h6_cost"] = cost6
#         print(fitness, rejected, cost)
#         print(fitness1, rejected1, cost1)
#         print(fitness2, rejected2, cost2)
#         print(fitness3, rejected3, cost3)
        with open (r"./result/result1_9_9_10.csv", "a") as f:
            fieldnames = ['dataset', 'h5_fitness', 'h5_rejected', 'h5_cost', 'h6_fitness', 'h6_rejected', 'h6_cost']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(result)
# # #         gen = {}
# # #         gen["dataset"] = path
# # #         gen["gen"] = sum_gen
# # #         with open (r"./result/result1_9_24_9_generation.csv", "a") as f:
# # #             fieldnames = ['dataset', 'gen']
# # #             writer = csv.DictWriter(f, fieldnames=fieldnames)
# # #             writer.writerow(gen)
            
# # #         MIP = {}
# # #         MIP["fitness_train"] = fitness_train
# # #         MIP["time_train"] = time_train
# # #         with open(r'./result/result1_9_24_9_MIP.csv', 'a') as f:
# # #             fieldnames = ['fitness_train', 'time_train']
# # #             writer = csv.DictWriter(f, fieldnames=fieldnames)
# # #             writer.writerow(MIP)
# #         covergence = {}
# #         covergence["decision"] = fitness_history["decision"]
# #         covergence["chosing"] = fitness_history["chosing"]
# #         with open(r'./result/result1_9_28_9_MIP.csv', 'a') as f:
# #             fieldnames = ['decision', 'chosing']
# #             writer = csv.DictWriter(f, fieldnames=fieldnames)
# #             writer.writerow(covergence)
            
            
#     path_nsf=[r'./data_1_9/conus_uniform_normal_s3.json', r'./data_1_9/conus_urban_hard_s2.json', r'./input_25/cogent_centers_easy_s3.json', r'./input_25/cogent_rural_hard_s3.json', r'./input_25/cogent_uniform_hard_s3.json']
#     for path in path_nsf:
#         print(path)
# #         result = {}
# #         result["dataset"] = path
#         fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, 100, 0.5, 5, 45, 2, 8, 4, 10, 100, 0.8, 0.1 )
        #print(fitness, rejected, cost)

#         fitness1, rejected1, cost1, proc1= heuristic1(path, 0.5, 10)

#         fitness2, rejected2, cost2, proc2 = heuristic2(path, 0.5, 10)

#         fitness3, rejected3, cost3, proc3 = heuristic3(path, 0.5, 10)

#         result["proposed_fitness"] = fitness
#         result["proposed_rejected"] = rejected
#         result["proposed_cost"] = cost
#         result["h1_fitness"] = fitness1
#         result["h1_rejected"] = rejected1
#         result["h1_cost"] = cost1
#         result["h2_fitness"] = fitness2
#         result["h2_rejected"] = rejected2
#         result["h2_cost"] = cost2
#         result["h3_fitness"] = fitness3
#         result["h3_rejected"] = rejected3
#         result["h3_cost"] = cost3
#         print(fitness, rejected, cost)
#         print(fitness1, rejected1, cost1)
#         print(fitness2, rejected2, cost2)
#         print(fitness3, rejected3, cost3)
#         with open (r"./result/result1_9_24_9.csv", "a") as f:
#             fieldnames = ['dataset', 'proposed_fitness', 'proposed_rejected', 'proposed_cost', 'h1_fitness', 'h1_rejected', 'h1_cost', 'h2_fitness', 'h2_rejected', 'h2_cost', 'h3_fitness', 'h3_rejected', 'h3_cost']
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writerow(result)
            
#         gen = {}
#         gen["dataset"] = path
#         gen["gen"] = sum_gen
#         with open (r"./result/result1_9_24_9_generation.csv", "a") as f:
#             fieldnames = ['dataset', 'gen']
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writerow(gen)
            
#         MIP = {}
#         MIP["fitness_train"] = fitness_train
#         MIP["time_train"] = time_train
#         with open(r'./result/result1_9_24_9_MIP.csv', 'a') as f:
#             fieldnames = ['fitness_train', 'time_train']
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writerow(MIP)
#         covergence = {}
#         covergence["decision"] = fitness_history["decision"]
#         covergence["chosing"] = fitness_history["chosing"]
#         with open(r'./result/result1_9_28_9_MIP.csv', 'a') as f:
#             fieldnames = ['decision', 'chosing']
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writerow(covergence)
        