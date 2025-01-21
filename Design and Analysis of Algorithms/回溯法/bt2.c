#include <stdio.h>
#include <string.h>

#define MAXN 20
#define MAXM 20
int n, m;
int connections[MAXN][MAXM];// connections[i][j]: 电路板i是否在连接块j中
int size[MAXN];             // 每个电路板的连接块数量
int used[MAXN];             // 电路板是否已被使用
int arrangement[MAXN];      // 当前排列
int best_arrangement[MAXN]; // 最佳排列
int best_length = MAXN;     // 最小长度

// 计算当前排列下每个连接块的长度，并返回最大长度
int len(int *arrangement){
    int max_len = 0;
    for(int j = 0; j < m; j++){
        int min_pos = MAXN;
        int max_pos = -1;
        for(int i = 0; i < n; i++){
            if(connections[arrangement[i]][j] == 1){
                if(i < min_pos)
                    min_pos = i;
                if(i > max_pos)
                    max_pos = i;
            }
        }
        if(max_pos != -1){
            int length = max_pos-min_pos;
            if(length > max_len)
                max_len = length;
        }
    }
    return max_len;
}
// 回溯法
void backtrack(int depth){
    if(depth == n){// 所有电路板已排列
        int current_length = len(arrangement);
        if(current_length < best_length){
            best_length = current_length;
            memcpy(best_arrangement, arrangement, sizeof(arrangement));
        }
        return;
    }
    for(int i = 0; i < n; i++){// 尝试将每个未使用的电路板放在当前深度
        if(!used[i]){
            used[i] = 1;
            arrangement[depth] = i;
            backtrack(depth + 1);
            used[i] = 0;
        }
    }
}

int main() {
    scanf("%d %d", &n, &m);
    for(int i = 0; i < n; i++){
        size[i] = 0;
        for(int j = 0; j < m; j++){
            int x;
            scanf("%d", &x);
            connections[i][j] = x;
            if (x == 1)
                size[i]++;
        }
    }
    memset(used, 0, sizeof(used));
    backtrack(0);
    printf("%d\n", best_length);
    for(int i = 0; i < n; i++)
        printf("%d ", best_arrangement[i] + 1);// 从1开始的排列
    return 0;
}