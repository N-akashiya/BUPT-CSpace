#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_N 100

// 优先队列节点
typedef struct {
    int level;          // 层次
    int weight;         // 权值
    int bound;          // 下界
    int x[MAX_N];       // 解向量
} Node;

int n, m;               // 顶点数，边数
int w[MAX_N];           // 顶点权值
int G[MAX_N][MAX_N];    // 邻接矩阵
Node *pq[10000];        // 优先队列
int pq_size = 0;        // 队列大小
int bestw = 0x7fffffff; // 最优解的权值
int bestx[MAX_N];       // 最优解

void swap(Node **a, Node **b) {
    Node *temp = *a;
    *a = *b;
    *b = temp;
}

void push(Node *node) {
    pq[pq_size] = node;
    int cur = pq_size;
    int parent = (cur-1)/2;
    while(cur>0 && pq[parent]->bound > pq[cur]->bound){
        swap(&pq[parent], &pq[cur]);
        cur = parent;
        parent = (cur-1)/2;
    }
    pq_size++;
}

Node *pop() {
    if(pq_size == 0) return NULL;
    Node *res = pq[0];
    pq[0] = pq[--pq_size];

    int cur = 0;
    while(1){
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
    int bound = node->weight; // 初始化为当前权值
    int *covered = (int *)calloc(n+1, sizeof(int));
    // 标记已覆盖的顶点
    for(int i=1; i<= node->level; i++){
        if(node->x[i]){
            for(int j=1; j<=n; j++){
                if(G[i][j])
                    covered[j] = 1;
            }
            covered[i] = 1;
        }
    }
    // 未覆盖的边，选择权值较小的顶点
    for(int i=1; i<= node->level; i++){
        for(int j=1; j<=n; j++){
            if(G[i][j] && !covered[i] && !covered[j])
                bound += (w[i]<w[j] ? w[i] : w[j]);
        }
    }
    free(covered);
    return bound;
}

int check(Node *node) {
    for(int i=1; i<=n; i++){
        for(int j=i+1; j<=n; j++){
            if(G[i][j] && !node->x[i] && !node->x[j])
                return 0;
        }
    }
    return 1;
}

void BranchBound() {
    Node *root = (Node *)malloc(sizeof(Node));
    memset(root->x, 0, sizeof(root->x));
    root->level = 0;
    root->weight = 0;
    root->bound = calc_bound(root);
    push(root);

    while(pq_size>0){
        Node *cur = pop();
        // 剪枝
        if(cur->bound >= bestw){
            free(cur);
            continue;
        }
        // 叶节点检查更新
        if(cur->level == n){
            if(check(cur) && cur->weight < bestw){
                bestw = cur->weight;
                memcpy(bestx, cur->x, sizeof(bestx));
            }
            free(cur);
            continue;
        }

        // 不选
        Node *left = (Node *)malloc(sizeof(Node));
        memcpy(left, cur, sizeof(Node));
        left->level++;
        left->bound = calc_bound(left);
        if(left->bound < bestw)
            push(left);
        else
            free(left);
        // 选择
        Node *right = (Node *)malloc(sizeof(Node));
        memcpy(right, cur, sizeof(Node));
        right->level++;
        right->x[right->level] = 1;
        right->weight += w[right->level];
        right->bound = calc_bound(right);
        if(right->bound < bestw && right->weight < bestw)
            push(right);
        else
            free(right);

        free(cur);
    }
}

int main() {
    scanf("%d %d", &n, &m);
    for(int i=1; i<=n; i++)
        scanf("%d", &w[i]);
    memset(G, 0, sizeof(G));
    for(int i=0; i<m; i++){
        int u, v;
        scanf("%d %d", &u, &v);
        G[u][v] = G[v][u] = 1;
    }
    BranchBound();
    printf("%d\n", bestw);
    for(int i=1; i<=n; i++)
        printf("%d ", bestx[i]);
    printf("\n");
    return 0;
}