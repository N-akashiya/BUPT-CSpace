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
        self.G = G                      # 图的邻接矩阵
        if flag == 0:
            self.best_cost = float('inf')
        else:
            self.best_cost = greedy_approximation(G, n)[0]

    def DP(self):
        # dp[mask][i] 表示访问过状态mask并且当前在城市i时的最小费用
        dp = [[float('inf')] * self.n for _ in range(1 << self.n)]
        dp[1][0] = 0 # 起点城市到自己的费用为0

        for mask in range(1 << self.n):
            for i in range(self.n):
                if mask & (1 << i): # 如果城市i在状态mask中被访问过
                    for j in range(self.n):
                        if mask & (1 << j) == 0: # 如果城市j没被访问过
                            new_mask = mask | (1 << j)
                            dp[new_mask][j] = min(dp[new_mask][j], dp[mask][i] + self.G[i][j])
        
        min_cost = float('inf')
        for i in range(1, self.n):
            min_cost = min(min_cost, dp[(1 << self.n) - 1][i] + self.G[i][0])
        # 更新最优值
        self.best_cost = min_cost

# 随机生成城市的邻接矩阵
def generate_matrix(num_cities, max_distance):
    matrix = [[0 if i == j else random.randint(1, max_distance) for j in range(num_cities)] for i in range(num_cities)]
    # 对称化（无向图）
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            matrix[j][i] = matrix[i][j]
    return matrix

def printG(G):
    for i in range(len(G)):
        print(G[i])

if __name__ == "__main__":
    n = 15
    m = 100
    G = generate_matrix(n, m)
    print("n =", n)

    tsp = Traveling(n, G)
    start = time.time()
    tsp.DP()
    end = time.time()
    print("动态规划求解")
    print("最短路径长度:", tsp.best_cost)
    print("运行时间：{:.2f}ms".format((end - start)*1000))
    
    flag = 1
    print("改进-动态规划求解")
    tsp = Traveling(n, G)
    print("近似最短路径长度:", tsp.best_cost)
    start = time.time()
    tsp.DP()
    end = time.time()
    print("最短路径长度:", tsp.best_cost)
    print("运行时间：{:.2f}ms".format((end - start)*1000))