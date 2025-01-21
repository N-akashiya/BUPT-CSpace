#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#define MAX_N 20

// 优先队列节点
typedef struct {
    int level;         // 层次
    int cost;          // 成本
    int bound;         // 下界
    int x[MAX_N];      // x[i]表示第i个元件安装的位置
    int used[MAX_N];   // 标记某位置是否被使用
} Node;

int n;                 // 元件数
int conn[MAX_N][MAX_N];// 连线矩阵
int dist[MAX_N][MAX_N];// 距离矩阵
int bestc = INT_MAX;   // 最优解的成本
int bestx[MAX_N];      // 最优解

Node* pq[10000];
int pq_size = 0;

void swap(Node **a, Node **b) {
    Node *temp = *a;
    *a = *b;
    *b = temp;
}

void push(Node *node) {
    pq[pq_size] = node;
    int cur = pq_size;
    int parent = (cur-1)/2;
    while(cur > 0 && pq[parent]->bound > pq[cur]->bound){
        swap(&pq[parent], &pq[cur]);
        cur = parent;
        parent = (cur-1)/2;
    }
    pq_size++;
}

Node* pop() {
    if(pq_size == 0) return NULL;
    Node *res = pq[0];
    pq[0] = pq[--pq_size];
    
    int cur = 0;
    while(1) {
        int left = cur*2+1;
        int right = cur*2+2;
        int min = cur;
        if(left < pq_size && pq[left]->bound < pq[min]->bound)
            min = left;
        if(right < pq_size && pq[right]->bound < pq[min]->bound) 
            min = right;
        if(min == cur)
            break;
        swap(&pq[cur], &pq[min]);
        cur = min;
    }
    return res;
}

int calc_bound(Node *node) {
    int bound = node->cost;
    int *used_pos = (int*)calloc(n, sizeof(int));
    for(int i=0; i<n; i++)
        used_pos[i] = node->used[i];
        
    // 对未处理元件计算最小可能成本
    for(int i=node->level; i<n; i++){
        int min_cost = INT_MAX;
        for(int j=0; j<n; j++){
            if(!used_pos[j]){
                int cost = 0;
                for(int k=0; k<node->level; k++)// 计算与已安排元件的成本
                    cost += conn[k][i] * dist[node->x[k]][j];
                if(cost < min_cost)
                    min_cost = cost;
            }
        }
        bound += min_cost;
    }
    free(used_pos);
    return bound;
}

void BranchBound() {
    Node *root = (Node*)malloc(sizeof(Node));
    for(int i=0; i<n; i++){
        root->x[i] = -1;
        root->used[i] = 0;
    }
    root->level = 0;
    root->cost = 0;
    root->bound = calc_bound(root);
    push(root);
    
    while(pq_size>0){
        Node *cur = pop();
        // 剪枝
        if(cur->bound >= bestc){
            free(cur);
            continue;
        }
        // 找到一个完整解
        if(cur->level == n){
            if(cur->cost < bestc){
                bestc = cur->cost;
                for(int i=0; i<n; i++)
                    bestx[i] = cur->x[i];
            }
            free(cur);
            continue;
        }
   
        // 扩展子节点
        for(int i=0; i<n; i++){
            if(!cur->used[i]){
                Node *next = (Node*)malloc(sizeof(Node));
                memcpy(next, cur, sizeof(Node));
                
                // 安排当前元件到位置i
                next->x[next->level] = i;
                next->used[i] = 1;
                next->level++;
                
                // 计算新增成本
                int new_cost = 0;
                for(int j=0; j<next->level-1; j++)
                    new_cost += conn[j][next->level-1] * dist[next->x[j]][i];
                next->cost += new_cost;
                
                next->bound = calc_bound(next);
                if(next->bound < bestc)
                    push(next);
                else
                    free(next);
            }
        }
        free(cur);
    }
}

int main() {
    scanf("%d", &n);
    for(int i=0; i<n-1; i++){
        for(int j=i+1; j<n; j++){
            scanf("%d", &conn[i][j]);
            conn[j][i] = conn[i][j];
        }
    }
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++)
            dist[i][j] = abs(i-j);
    }
    BranchBound();
    printf("%d\n", bestc);
    for(int i=0; i<n; i++)
        printf("%d ", bestx[i]+1);
    printf("\n");
    return 0;
}