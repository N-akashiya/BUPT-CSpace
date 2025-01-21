#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 100
int n, m;
int enemies[MAXN+1][MAXN];// enemies[u][v]: 居民u和居民v是否是仇敌
int best_cnt = 0;         // 最多入伍居民数量
int cnt = 0;              // 当前入伍居民数量
int best_solution[MAXN+1];// 最佳方案
int solution[MAXN+1];     // 当前方案

void backtrack(int resident){
    if(resident > n){// 如果所有居民都已处理完
        if(cnt > best_cnt){
            best_cnt = cnt;
            memcpy(best_solution, solution, sizeof(solution));
        }
        return;
    }
    
    if(cnt + (n - resident + 1) <= best_cnt)// 剪枝
        return;

    int can_join = 1;// 是否可以入伍
    for(int i = 1; i <= n; i++){// 检查仇敌关系
        if(solution[i] == 1 && enemies[resident][i] == 1){
            can_join = 0;
            break;
        }
    }
    // 尝试入伍
    if(can_join){
        solution[resident] = 1;
        cnt++;
        backtrack(resident + 1);
        solution[resident] = 0;// 回溯
        cnt--;
    }
    // 不入伍
    solution[resident] = 0;
    backtrack(resident + 1);
}

int main(){
    scanf("%d %d", &n, &m);

    memset(enemies, 0, sizeof(enemies));
    memset(best_solution, 0, sizeof(best_solution));
    memset(solution, 0, sizeof(solution));

    for(int i = 0; i < m; i++){
        int u, v;
        scanf("%d %d", &u, &v);
        enemies[u][v] = 1;
        enemies[v][u] = 1;
    }
    backtrack(1);
    printf("%d\n", best_cnt);
    for(int i = 1; i <= n; i++)
        printf("%d ", best_solution[i]);
    return 0;
}