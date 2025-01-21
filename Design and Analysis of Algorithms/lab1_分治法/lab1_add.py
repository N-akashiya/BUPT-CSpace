import random
import time
import os
import matplotlib.pyplot as plt

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
def benchmark(repetition):
    n = 1000000
    algorithms = [RandomizedSelect, Select]
    k = 8
    res = {}
    
    for alg in algorithms:
        print(f"Algorithm = {alg.__name__}:")
        times = []
        A = list(range(n))
        random.shuffle(A)
        for _ in range(repetition):
            start = time.time()
            alg(A, 0, n-1, n-k)# 找第k大的数
            end = time.time()
            times.append((end - start)*1000)
            print(f"run {_+1}: {times[-1]:.4f}ms")
        res[alg.__name__] = times
    return res

def plot(res):
    if not os.path.exists('figure'):
        os.makedirs('figure')

    for alg in ["RandomizedSelect", "Select"]:
        plt.figure(figsize=(10, 6))
        times = res[alg]
        repetition = range(1, len(times)+1)
        
        plt.plot(repetition, times, label=f"n = 1000000", marker='o')
        plt.title(f"Performance of {alg} for n=1000000")
        plt.xlabel("number of searches")
        plt.ylabel("time (ms)")
        plt.grid(True, ls="--")
        plt.savefig(os.path.join('figure', f'Performance_{alg}_k_8.png'))
        plt.close()

results = benchmark(15)
plot(results)