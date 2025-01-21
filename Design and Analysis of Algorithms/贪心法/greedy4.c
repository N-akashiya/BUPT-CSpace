#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    return *(int *)a - *(int *)b;
}

double greedy(int n, int p[]) {
    qsort(p, n, sizeof(int), cmp);
    int x[n];
    int k = n/2;
    // 最大的放中间
    x[k] = p[n-1];
    // 两边交替放
    for(int i=k+1; i<n; i++)
        x[i] = p[n-2*(i-k)];
    for(int i=k-1; i>=0; i--)
        x[i] = p[n-2*(k-i)-1];
    
    double m=0, t=0;
    for(int i=0; i<n; i++){
        m += p[i];
        for(int j=i+1; j<n; j++)
            t += x[i]*x[j]*(j-i);
    }
    t = t/m/m;
    return t;
}

int main() {
    int n;
    scanf("%d", &n);
    int a[n];
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);
        
    double res = greedy(n, a);
    printf("%.6f\n", res);
    return 0;
}