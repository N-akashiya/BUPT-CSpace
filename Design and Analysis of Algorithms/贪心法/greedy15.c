#include <stdio.h>

int dicomp(int n) {
    int k = 2; // 从2开始分解
    int a[n/2];
    int index = 0;
    while(n > 0){
        if(n-k >= 0){
            a[index++] = k;
            n -= k;
            k++;
        } 
        else{
            a[index] = n;
            n = 0;
        }
    }
    int remain = a[index];
    // 从后往前，将剩余的数均匀分配
    for(int i = index-1; i>=0 && remain>0; i--){
        a[i]++;
        remain--;
    }
    int res = 1;
    for(int i = 0; i < index; i++)
        res *= a[i];
    return res;
}

int main() {
    int n;
    scanf("%d", &n);
    printf("%d", dicomp(n));
}