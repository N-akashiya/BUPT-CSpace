import random
import time
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def tsp_or_tools(G):
    data = {
        'distance_matrix': G,
        'num_vehicles': 1,
        'depot': 0
    }

    # 创建路由模型
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        # 返回从点 `from_index` 到点 `to_index` 的距离
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 设置搜索参数
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.seconds = 10  # 最大运行时间（秒）

    # 求解问题
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(route[0])  # 回到起点
        cost = solution.ObjectiveValue()
        return cost, route
    else:
        return None, None

def greedy_approximation(G, n):
    visited = [False] * n
    current_city = 0
    visited[current_city] = True
    total_cost = 0
    path = [current_city]

    for _ in range(n - 1):
        next_city = None
        min_cost = float('inf')
        for j in range(n):
            if not visited[j] and G[current_city][j] < min_cost:
                min_cost = G[current_city][j]
                next_city = j
        visited[next_city] = True
        total_cost += min_cost
        current_city = next_city
        path.append(current_city)

    total_cost += G[current_city][path[0]]
    path.append(path[0])
    return total_cost, path

def calculate_cost(G, path):
    return sum(G[path[i]][path[i + 1]] for i in range(len(path) - 1))

def simulated_annealing(G, n, initial_temperature, cooling_rate, iteration_per_temp):
    # 初始解: 贪心算法
    _, path = greedy_approximation(G, n)
    cost = calculate_cost(G, path)

    best_path = path[:]
    best_cost = cost

    temperature = initial_temperature
    stable_iterations = 0 # 稳定计数

    while temperature > 1e-3: # 终止条件: 温度接近于零
        update = False
        for _ in range(iteration_per_temp):
            neighborhood = [] # 邻域
            for _ in range(100):
                new_path = path[:]
                i, j = random.sample(range(1, n), 2) # 保证起点不参与交换
                new_path[i], new_path[j] = new_path[j], new_path[i]
                neighborhood.append((calculate_cost(G, new_path), new_path))
            # 选择最优解作为当代最优解
            neighborhood.sort(key=lambda x: x[0])
            best_local_cost, best_local_path = neighborhood[0]
            # 判断是否接受当代最优解
            if best_local_cost < cost or random.random() < math.exp(-(best_local_cost - cost) / (temperature * 0.1)):
                path = best_local_path
                cost = best_local_cost
                update = True
                # 更新全局最优解
                if cost < best_cost:
                    best_path = path[:]
                    best_cost = cost
        if not update:
            stable_iterations += 1
            if stable_iterations >= 10:
                break
        else:
            stable_iterations = 0    
        # 温度递减
        temperature *= cooling_rate

    return best_cost, best_path

# 随机生成城市的邻接矩阵
def generate_matrix(num_cities, max_distance):
    matrix = [[0 if i == j else random.randint(1, max_distance) for j in range(num_cities)] for i in range(num_cities)]
    # 对称化（无向图）
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            matrix[j][i] = matrix[i][j]
    return matrix

if __name__ == "__main__":
    n = 50
    m = 100
    G = generate_matrix(n, m)
    print("n =", n)

    initial_temperature = max(max(G)) * n
    cooling_rate = 0.995
    iteration_per_temp = 100
    start = time.time()
    best_cost, best_path = simulated_annealing(G, n, initial_temperature, cooling_rate, iteration_per_temp)
    end = time.time()
    print("模拟退火算法求解")
    print("近似的最短路径长度:", best_cost)
    print("近似的最短路径:", best_path)
    print("运行时间：{:.4f}s".format(end - start))

    start = time.time()
    cost, route = tsp_or_tools(G)
    end = time.time()
    print("OR-Tools TSP解法")
    print("最短路径长度:", cost)
    print("最短路径:", route)
    print("运行时间：{:.4f}s".format(end - start))