#include <stdio.h>
#include <limits.h>

#define MAX_N 100
int N, K, A, B, C;
int memo[MAX_N+1][MAX_N+1][2];
int map[MAX_N+1][MAX_N+1];

void init_memo(){
    for(int i=1; i<=N; i++){
        for(int j=1; j<=N; j++){
            memo[i][j][0] = INT_MAX;
            memo[i][j][1] = -1;
        }
    }
    memo[1][1][0] = 0;
    memo[1][1][1] = K;
}

void update_memo(){
    int s[4][3] = {{0, -1, 0}, {-1, 0, 0}, {0, 1, B}, {1, 0, B}};
    int update;
    do{
        update = 0;
        for(int x=1; x<=N; x++){
            for(int y=1; y<=N; y++){
                if(x==1 && y==1)
                    continue;
                for(int i=0; i<4; i++){
                    int nx = x+s[i][0];
                    int ny = y+s[i][1];
                    if(nx<1 || nx>N || ny<1 || ny>N)
                        continue;
                    int cost = memo[nx][ny][0]+s[i][2];
                    int fuel = memo[nx][ny][1]-1;
                    if(fuel < 0) 
                        continue;
                    // 加油
                    if(map[x][y] == 1){
                        cost += A;
                        fuel = K;
                    }
                    // 需要新建油库
                    if(fuel == 0 && (x!=N || y!=N)){
                        cost += A+C;
                        fuel = K;
                    }
                    // 更新
                    if(cost<memo[x][y][0] || (cost==memo[x][y][0] && fuel>memo[x][y][1])){
                        memo[x][y][0] = cost;
                        memo[x][y][1] = fuel;
                        update = 1;
                    }
                }
            }
        }
    }while(update);
}

int main(){
    scanf("%d %d %d %d %d", &N, &K, &A, &B, &C);
    for(int i=1; i<=N; i++){
        for(int j=1; j<=N; j++)
            scanf("%d", &map[i][j]);
    }
    init_memo();
    update_memo();
    printf("%d\n", memo[N][N][0]);
    return 0;
}