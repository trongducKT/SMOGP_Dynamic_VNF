from run import heuristic3, heuristic4, heuristic5, heuristic6
import csv

if __name__ == '__main__':
    path_nsf = [r'./input_25/cogent_uniform_normal_s3.json', r'./input_25/cogent_urban_easy_s1.json', r'./input_25/cogent_urban_easy_s2.json', r'./input_25/cogent_urban_easy_s3.json', r'./input_25/cogent_urban_hard_s1.json', r'./input_25/cogent_urban_hard_s2.json', r'./input_25/cogent_urban_hard_s3.json',r'./input_25/cogent_urban_normal_s1.json', r'./input_25/cogent_urban_normal_s2.json', r'./input_25/cogent_urban_normal_s3.json', r'./data_1_9/nsf_centers_easy_s1.json', r'./data_1_9/nsf_centers_easy_s2.json',r'./data_1_9/nsf_centers_easy_s3.json', r'./data_1_9/nsf_centers_hard_s1.json', r'./data_1_9/nsf_centers_hard_s2.json',r'./data_1_9/nsf_centers_hard_s3.json', r'./data_1_9/nsf_centers_normal_s1.json',r'./data_1_9/nsf_centers_normal_s2.json', r'./data_1_9/nsf_centers_normal_s3.json',r'./data_1_9/nsf_rural_easy_s1.json', r'./data_1_9/nsf_rural_easy_s2.json', r'./data_1_9/nsf_rural_easy_s3.json', r'./data_1_9/nsf_rural_hard_s1.json', r'./data_1_9/nsf_rural_hard_s2.json', r'./data_1_9/nsf_rural_hard_s3.json', r'./data_1_9/nsf_rural_normal_s1.json', r'./data_1_9/nsf_rural_normal_s2.json', r'./data_1_9/nsf_rural_normal_s3.json', r'./data_1_9/nsf_uniform_easy_s1.json', r'./data_1_9/nsf_uniform_easy_s2.json', r'./data_1_9/nsf_uniform_easy_s3.json', r'./data_1_9/nsf_uniform_hard_s1.json', r'./data_1_9/nsf_uniform_hard_s2.json', r'./data_1_9/nsf_uniform_hard_s3.json', r'./data_1_9/nsf_uniform_normal_s1.json', r'./data_1_9/nsf_uniform_normal_s2.json', r'./data_1_9/nsf_uniform_normal_s3.json', r'./data_1_9/nsf_urban_easy_s1.json', r'./data_1_9/nsf_urban_easy_s2.json', r'./data_1_9/nsf_urban_easy_s3.json', r'./data_1_9/nsf_urban_hard_s1.json', r'./data_1_9/nsf_urban_hard_s2.json', r'./data_1_9/nsf_urban_hard_s3.json',r'./data_1_9/nsf_urban_normal_s1.json', r'./data_1_9/nsf_urban_normal_s2.json', r'./data_1_9/nsf_urban_normal_s3.json',r'./data_1_9/conus_centers_easy_s1.json', r'./data_1_9/conus_centers_easy_s2.json',r'./data_1_9/conus_centers_easy_s3.json', r'./data_1_9/conus_centers_hard_s1.json', r'./data_1_9/conus_centers_hard_s2.json',r'./data_1_9/conus_centers_hard_s3.json', r'./data_1_9/conus_centers_normal_s1.json',r'./data_1_9/conus_centers_normal_s2.json', r'./data_1_9/conus_centers_normal_s3.json',r'./data_1_9/conus_rural_easy_s1.json', r'./data_1_9/conus_rural_easy_s2.json', r'./data_1_9/conus_rural_easy_s3.json', r'./data_1_9/conus_rural_hard_s1.json', r'./data_1_9/conus_rural_hard_s2.json', r'./data_1_9/conus_rural_hard_s3.json', r'./data_1_9/conus_rural_normal_s1.json', r'./data_1_9/conus_rural_normal_s2.json', r'./data_1_9/conus_rural_normal_s3.json', r'./data_1_9/conus_uniform_easy_s1.json', r'./data_1_9/conus_uniform_easy_s2.json', r'./data_1_9/conus_uniform_easy_s3.json', r'./data_1_9/conus_uniform_hard_s1.json', r'./data_1_9/conus_uniform_hard_s2.json', r'./data_1_9/conus_uniform_hard_s3.json', r'./data_1_9/conus_uniform_normal_s1.json', r'./data_1_9/conus_uniform_normal_s2.json', r'./data_1_9/conus_uniform_normal_s3.json', r'./data_1_9/conus_urban_easy_s1.json', r'./data_1_9/conus_urban_easy_s2.json', r'./data_1_9/conus_urban_easy_s3.json', r'./data_1_9/conus_urban_hard_s1.json', r'./data_1_9/conus_urban_hard_s2.json', r'./data_1_9/conus_urban_hard_s3.json',r'./data_1_9/conus_urban_normal_s1.json', r'./data_1_9/conus_urban_normal_s2.json', r'./data_1_9/conus_urban_normal_s3.json',r'./input_25/cogent_centers_easy_s1.json', r'./input_25/cogent_centers_easy_s2.json',r'./input_25/cogent_centers_easy_s3.json', r'./input_25/cogent_centers_hard_s1.json', r'./input_25/cogent_centers_hard_s2.json',r'./input_25/cogent_centers_hard_s3.json', r'./input_25/cogent_centers_normal_s1.json',r'./input_25/cogent_centers_normal_s2.json', r'./input_25/cogent_centers_normal_s3.json',r'./input_25/cogent_rural_easy_s1.json', r'./input_25/cogent_rural_easy_s2.json', r'./input_25/cogent_rural_easy_s3.json', r'./input_25/cogent_rural_hard_s1.json', r'./input_25/cogent_rural_hard_s2.json', r'./input_25/cogent_rural_hard_s3.json', r'./input_25/cogent_rural_normal_s1.json', r'./input_25/cogent_rural_normal_s2.json', r'./input_25/cogent_rural_normal_s3.json', r'./input_25/cogent_uniform_easy_s1.json', r'./input_25/cogent_uniform_easy_s2.json', r'./input_25/cogent_uniform_easy_s3.json', r'./input_25/cogent_uniform_hard_s1.json', r'./input_25/cogent_uniform_hard_s2.json', r'./input_25/cogent_uniform_hard_s3.json', r'./input_25/cogent_uniform_normal_s1.json', r'./input_25/cogent_uniform_normal_s2.json' ]
    for path in path_nsf:
        print(path)
        result = {}
        result["dataset"] = path 
        
#         fitness3, rejected3, cost3, proc3= heuristic3(path, 0.5, 10)

        fitness4, rejected4, cost4, proc4 = heuristic4(path, 0.5, 10)

#         fitness5, rejected5, cost5, proc5 = heuristic5(path, 0.5, 10)
        
#         fitness6, rejected6, cost6, proc6 = heuristic6(path, 0.5, 10)
        
#         result["h3_fitness"] = fitness3
#         result["h3_rejected"] = rejected3
#         result["h3_cost"] = cost3
        result["h4_fitness"] = fitness4
        result["h4_rejected"] = rejected4
        result["h4_cost"] = cost4
#         result["h5_fitness"] = fitness5
#         result["h5_rejected"] = rejected5
#         result["h5_cost"] = cost5
#         result["h6_fitness"] = fitness6
#         result["h6_rejected"] = rejected6
#         result["h6_cost"] = cost6
        
        with open (r"./result/result_heuristic_heuris3.csv", "a") as f:
#             fieldnames = ['dataset', 'h3_fitness', 'h3_rejected', 'h3_cost', 'h4_fitness', 'h4_rejected', 'h4_cost', 'h5_fitness', 'h5_rejected', 'h5_cost', 'h6_fitness', 'h6_rejected', 'h6_cost']
            fieldnames = ['dataset', 'h4_fitness', 'h4_rejected', 'h4_cost']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(result)
               