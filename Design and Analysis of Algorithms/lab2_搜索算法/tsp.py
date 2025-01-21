import random

class Traveling:
    def __init__(self, n, G):
        self.n = n                      # 图的顶点数
        self.sol = [i for i in range(n)]# 当前解
        self.best_sol = []              # 当前最优解
        self.G = G                      # 图的邻接矩阵
        self.cost = 0                   # 当前费用
        self.best_cost = float('inf')   # 当前最优值
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
    n = 10
    m = 100
    G = generate_matrix(n, m)
    print("城市邻接矩阵")
    printG(G)

    tsp = Traveling(n, G)
    tsp.Backtrack(0)
    print("回溯法求解")
    print("最短路径长度:", tsp.best_cost)
    print("最短路径:")
    for path in tsp.best_sol:
        if path[0] == 0:
            print(path + [0])

    tsp = Traveling(n, G)
    tsp.DP()
    print("动态规划求解")
    print("最短路径长度:", tsp.best_cost)
