#include <stdio.h>
#include <string.h>

#define MAX_SYMBOLS 20
typedef struct {
    char stack[50];
    char input[50];
}AnalysisStep;
char non_terms[] = {'E', 'A', 'T', 'B', 'F'};
char terms[] = {'+', '-', '*', '/', '(', ')', 'n', 'e', '$'};
char FIRST[5][MAX_SYMBOLS] = {{0}};
char FOLLOW[5][MAX_SYMBOLS] = {{0}};
int LL1Table[5][9] = {{0}};
const char* productions[] = {
    "E->TA",
    "A->+TA",
    "A->-TA",
    "A->e",
    "T->FB",
    "B->*FB",
    "B->/FB",
    "B->e",
    "F->(E)",
    "F->n"
};

int add_to_set(char set[], char sym){
    if(!strchr(set, sym)){
        int len = strlen(set);
        set[len] = sym;
        set[len+1] = '\0';
        return 1;
    }
    return 0;
}

void first(){
    int update = 1;
    while(update){
        update = 0;
        for(int i=0; i<10; i++){
            char left = productions[i][0];
            const char* right = productions[i]+3;
            int index = strchr(non_terms, left) - non_terms;
            if(strchr(terms, right[0]))// 如果右部第一个符号是终结符
                update |= add_to_set(FIRST[index], right[0]);
            else{
                for(int j=0; right[j]!='\0'; j++){
                    if(strchr(terms, right[j])){
                        update |= add_to_set(FIRST[index], right[j]);
                        break;
                    }
                    int right_index = strchr(non_terms, right[j]) - non_terms;
                    for(int k=0; FIRST[right_index][k]!='\0'; k++){
                        char sym = FIRST[right_index][k];
                        if(sym != 'e')
                            update |= add_to_set(FIRST[index], sym);
                    }
                    if(!strchr(FIRST[right_index], 'e'))// 不包含空串
                        break;
                }   
            }
        }
    }
}

void follow(){
    add_to_set(FOLLOW[0], '$');
    int update = 1;
    while(update){
        update = 0;
        for(int i=0; i<10; i++){
            char left = productions[i][0];
            const char* right = productions[i]+3;
            for(int j=0; right[j]!='\0'; j++){
                if(strchr(non_terms, right[j])){// 右部非终结符
                    int index = strchr(non_terms, right[j]) - non_terms;
                    // 后面还有符号
                    if(right[j+1] != '\0'){
                        if(strchr(terms, right[j+1]))// 是终结符
                            update |= add_to_set(FOLLOW[index], right[j+1]);
                        else{
                            int right_index = strchr(non_terms, right[j+1]) - non_terms;
                            for(int k=0; FIRST[right_index][k]!='\0'; k++){
                                char sym = FIRST[right_index][k];
                                if(sym != 'e')
                                    update |= add_to_set(FOLLOW[index], sym);
                            }
                            if(strchr(FIRST[right_index], 'e')){// 包含空串
                                int left_index = strchr(non_terms, left) - non_terms;
                                for(int k=0; FOLLOW[left_index][k]!='\0'; k++)
                                    update |= add_to_set(FOLLOW[index], FOLLOW[left_index][k]);
                            }
                        }
                    }
                    else{
                        int left_index = strchr(non_terms, left) - non_terms;
                        for(int k=0; FOLLOW[left_index][k]!='\0'; k++)
                            update |= add_to_set(FOLLOW[index], FOLLOW[left_index][k]);
                    }
                }
            }
        }
    }
}

void ll1table(){
    // 初始化表项为0：ERROR
    for(int i=0; i<10; i++){
        char left = productions[i][0];
        const char* right = productions[i]+3;
        int n_index = strchr(non_terms, left) - non_terms;

        if(strchr(terms, right[0])){// 右部第一个符号是终结符
            if(right[0] == 'e'){
                for(int j=0; FOLLOW[n_index][j]!='\0'; j++){
                    char b = FOLLOW[n_index][j];
                    int b_index = strchr(terms, b) - terms;
                    LL1Table[n_index][b_index] = i+1;
                }
            }
            else{
                int a_index = strchr(terms, right[0]) - terms;
                LL1Table[n_index][a_index] = i+1;
            }
        }
        else{
            // 需要逐个展开，直到找到终结符
            for(int j=0; right[j]!='\0'; j++){
                int al_index = strchr(non_terms, right[0]) - non_terms;
                int flag = 0;// 是否包含空串
                for(int k=0; FIRST[al_index][k]!='\0'; k++){
                    char a = FIRST[al_index][k];
                    if(a != 'e'){
                        int a_index = strchr(terms, a) - terms;
                        LL1Table[n_index][a_index] = i+1;
                    }
                    else
                        flag=1;
                }
                if(!flag)
                    break;
            }
            int al_index = strchr(non_terms, right[0]) - non_terms;
            if(strchr(FIRST[al_index], 'e')){// 推导出空串
                for(int k=0; FOLLOW[n_index][k]!='\0'; k++){
                    char b = FOLLOW[n_index][k];
                    int b_index = strchr(terms, b) - terms;
                    LL1Table[n_index][b_index] = i+1;
                }
            }
        }
    }    
}

void print_ll1table() {
    printf("LL(1) Table:\n");
    printf("    ");
    for (int i = 0; i < 9; i++) {
        printf("%c ", terms[i]);
    }
    printf("\n");
    for (int i = 0; i < 5; i++) {
        printf("%c | ", non_terms[i]);
        for (int j = 0; j < 9; j++) {
            if (LL1Table[i][j] == 0) {
                printf("  ");
            } else {
                printf("%d ", LL1Table[i][j]);
            }
        }
        printf("\n");
    }
}

void ll1analyze(char* expr){
    AnalysisStep steps;
    int top = 1;// 分析栈栈顶
    int ip = 0;// 向前指针
    steps.stack[0] = '$';
    steps.stack[1] = 'E';
    strcpy(steps.input, expr);
    strcat(steps.input, "$");
    
    char X = steps.stack[top];// 分析栈顶符号
    do{
        X = steps.stack[top];
        char a = steps.input[ip];// 输入栈顶符号
        for(int i=0; i<=top; i++)
            printf("%c", steps.stack[i]);
        printf("\t");
        printf("%s\t", steps.input+ip);
        
        if(strchr(terms, X)){ // X是终结符或$
            if(X==a){
                if(X=='$')
                    printf("accept\n");
                else
                    printf("match\n");
                top--;// pop
                ip++;
            }
            else{
                printf("error\n");
                return;
            }
        }
        else{
            int X_index = strchr(non_terms, X) - non_terms;
            int a_index = strchr(terms, a) - terms;
            if(LL1Table[X_index][a_index]){
                int p_index = LL1Table[X_index][a_index] - 1;
                printf("%d\n", p_index+1);
                top--;// pop
                const char* right = productions[p_index]+3;
                // 反向入分析栈
                for(int i=strlen(right)-1; i>=0; i--){
                    if(right[i] != 'e')
                        steps.stack[++top] = right[i];
                }
            }
            else{
                printf("error\n");
                return;
            }
        }
    }while(X!='$');// 分析栈非空，继续
}

int main(){
    first();
    follow();
    ll1table();
    // print_ll1table();
    char expr[100];
    scanf("%99s", expr);
    ll1analyze(expr);
    return 0;
}