import random
import time
import os
import matplotlib.pyplot as plt
from fractions import Fraction

# 随机选择
def RandomizedPartition(A, p, r):
    def Partition(A, p, r):
        x = A[r]
        i = p-1
        for j in range(p, r):
            if A[j] <= x:
                i += 1
                A[i], A[j] = A[j], A[i]
        A[i+1], A[r] = A[r], A[i+1]
        return i+1
    
    pivot = random.randint(p, r)
    A[r], A[pivot] = A[pivot], A[r]
    return Partition(A, p, r)

def RandomizedSelect(A, p, r, k):
    if p == r:
        return A[p]
    i = RandomizedPartition(A, p, r)
    j = i-p+1
    if k <= j:
        return RandomizedSelect(A, p, i, k)
    else:
        return RandomizedSelect(A, i+1, r, k-j)

# 线性时间选择
def Select(A, p, r, k):
    def Partition(A, p, r, x):
        for j in range(p, r+1):
            if A[j] == x:
                A[j], A[r] = A[r], A[j]
                break
        x = A[r]
        i = p-1
        for j in range(p, r):
            if A[j] <= x:
                i += 1
                A[i], A[j] = A[j], A[i]
        A[i+1], A[r] = A[r], A[i+1]
        return i+1

    if (r-p) < 75:
        A[p:r+1] = sorted(A[p:r+1])
        return A[p+k-1]
    
    for i in range((r-p-4)//5):
        # 取出A[p+i*5:p+i*5+4]的中位数与A[p+i]交换
        right = min(p+i*5+4, r)
        median = sorted(A[p+i*5 : right+1])[len(A[p+i*5 : right+1])//2]
        median_index = A.index(median, p+i*5, right+1)
        A[p+i], A[median_index] = A[median_index], A[p+i]
        # 求中位数的中位数
        median_of_medians = Select(A, p, p+(r-p)//5, (r-p)//10)
        i = Partition(A, p, r, median_of_medians)
        j = i-p+1
        if k <= j:
            return Select(A, p, i, k)
        else:
            return Select(A, i+1, r, k-j)

# 测试
def benchmark():
    size = [1000, 100000, 1000000, 10000000]
    algorithms = [RandomizedSelect, Select]
    res = {}

    for n in size:
        res[n] = {}
        step = n//8
        for pos in range(0, 9):
            k = pos*step-1 if pos > 0 else 0
            if k == 0:
                k_label = "1"
            else:
                k_label = f"{Fraction(pos, 8)} n" if pos != 8 else "n"
            res[n][k_label] = {}
            for alg in algorithms:
                A = list(range(n))
                random.shuffle(A)
                start = time.time()
                alg(A, 0, n-1, n-k)# 找第k大的数
                end = time.time()
                res[n][k_label][alg.__name__] = end - start
                print(f"n = {n}, k = {k_label}, {alg.__name__}, time = {end - start:.4f}s")
    return res

def plot(res):
    if not os.path.exists('figure'):
        os.makedirs('figure')

    for alg in ["RandomizedSelect", "Select"]:
        plt.figure(figsize=(10, 6))
        for n in res.keys():
            x = list(res[n].keys())
            y = [res[n][k][alg] for k in x]
            plt.plot(x, y, label=f"n = {n}", marker='o')
        plt.title(f"Performance of {alg}")
        plt.xlabel("k (position in array)")
        plt.ylabel("time (s)")
        plt.yscale('log')
        plt.legend(loc='lower right')
        plt.grid(True, ls="--")
        plt.savefig(os.path.join('figure', f'Performance_{alg}.png'))
        plt.close()

results = benchmark()
plot(results)