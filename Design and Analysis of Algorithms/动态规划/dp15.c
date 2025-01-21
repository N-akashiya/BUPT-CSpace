#include <stdio.h>
#include <string.h>

#define max(a, b) ((a) > (b) ? (a) : (b))

void update(int x1, int y1, int x2, int y2, int n, int v[n][n], int h[n][n][n][n]){
    int max_val = 0;
    if(x1>0 && x2>0) max_val = max(max_val, h[x1-1][y1][x2-1][y2]);
    if(x1>0 && y2>0) max_val = max(max_val, h[x1-1][y1][x2][y2-1]);
    if(y1>0 && x2>0) max_val = max(max_val, h[x1][y1-1][x2-1][y2]);
    if(y1>0 && y2>0) max_val = max(max_val, h[x1][y1-1][x2][y2-1]);
    // 更新
    h[x1][y1][x2][y2] = max_val + v[x1][y1];
    if(x1 != x2 || y1 != y2)// 如果路径不重合
        h[x1][y1][x2][y2] += v[x2][y2];
}

int main(){
    int n;
    scanf("%d", &n);
    int v[n][n];
    int h[n][n][n][n];
    memset(v, 0, sizeof(v));
    memset(h, 0, sizeof(h));

    int x, y, value;
    while(scanf("%d %d %d", &x, &y, &value) && (x!=0 || y!=0 || value!=0)){
        v[x-1][y-1] = value;
    }
    h[0][0][0][0] = v[0][0];// A点

    for(int x1=0; x1<n; x1++){
        for(int y1=0; y1<n; y1++){
            for(int x2=0; x2<n; x2++){
                for(int y2=0; y2<n; y2++){
                    if(x1==0 && y1==0 && x2==0 && y2==0) 
                        continue;
                    if(x1+y1 == x2+y2)
                        update(x1, y1, x2, y2, n, v, h);
                }
            }
        }
    }
    printf("%d\n", h[n-1][n-1][n-1][n-1]);
    return 0;
}