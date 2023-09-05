from run import run_proposed, heuristic2, heuristic3, heuristic1


if __name__ == '__main__':



    path = r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data_1_9\nsf_centers_hard_s3.json'
    fitness, rejected, cost = run_proposed(path, 4, 0.5, 10, 10, 2, 8, 4, 10, 20, 0.8, 0.1)
    #print(fitness, rejected, cost)

    fitness1, rejected1, cost1 = heuristic1(path, 0.5, 10)
        
    fitness2, rejected2, cost2 = heuristic2(path, 0.5, 10)

        
    fitness3, rejected3, cost3 = heuristic3(path, 0.5, 10)
        
    print(fitness, rejected, cost)
    print(fitness1, rejected1, cost1)
    print(fitness2, rejected2, cost2)
    print(fitness3, rejected3, cost3)