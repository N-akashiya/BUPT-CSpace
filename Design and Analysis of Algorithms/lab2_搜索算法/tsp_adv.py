import random
import time
flag = 0

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

class Traveling:
    def __init__(self, n, G):
        self.n = n                      # 图的顶点数
        self.sol = [i for i in range(n)]# 当前解
        self.best_sol = []              # 当前最优解
        self.G = G                      # 图的邻接矩阵
        self.cost = 0                   # 当前费用
        if flag == 0:
            self.best_cost = float('inf')
        else:
            self.best_cost = greedy_approximation(G, n)[0]
        self.visited = [False] * n      # 访问标记

    def Backtrack(self, i):
        if i == self.n: # 当所有顶点都被访问完毕
            cost = self.cost + self.G[self.sol[-1]][self.sol[0]] # 回到起点的费用
            if cost < self.best_cost: # 更新最优值
                self.best_cost = cost
                self.best_sol = [self.sol[:]]
            elif cost == self.best_cost: # 添加解
                self.best_sol.append(self.sol[:])
        else:
            for j in range(self.n): # 遍历所有顶点
                if not self.visited[j]: # 判断是否可行
                    # 剪枝
                    if i > 0 and self.cost + self.G[self.sol[i - 1]][j] > self.best_cost:
                        continue
                    self.visited[j] = True
                    self.sol[i] = j
                    if i == 0:
                        self.cost = 0
                    else:
                        self.cost += self.G[self.sol[i - 1]][self.sol[i]]
                    self.Backtrack(i + 1) # 递归进入下一层
                    if i > 0:
                        self.cost -= self.G[self.sol[i - 1]][self.sol[i]]
                    self.visited[j] = False

# 随机生成城市的邻接矩阵
def generate_matrix(num_cities, max_distance):
    matrix = [[0 if i == j else random.randint(1, max_distance) for j in range(num_cities)] for i in range(num_cities)]
    # 对称化（无向图）
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            matrix[j][i] = matrix[i][j]
    return matrix

if __name__ == "__main__":
    n = 11
    m = 100
    G = generate_matrix(n, m)
    print("n =", n)

    tsp = Traveling(n, G)
    start = time.time()
    tsp.Backtrack(0)
    end = time.time()
    print("回溯法求解")
    print("最短路径长度:", tsp.best_cost)
    print("运行时间：{:.2f}ms".format((end - start)*1000))
    
    flag = 1
    print("改进-回溯法求解")
    tsp = Traveling(n, G)
    print("近似最短路径长度:", tsp.best_cost)
    start = time.time()
    tsp.Backtrack(0)
    end = time.time()
    print("最短路径长度:", tsp.best_cost)
    print("运行时间：{:.2f}ms".format((end - start)*1000))
    