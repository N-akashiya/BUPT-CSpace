#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SYMBOLS 30
#define MAX_STATES 50
typedef struct {
    char stack[MAX_STATES];
    char input[MAX_STATES];
}AnalysisStep;
typedef struct {
    char left;
    char right[MAX_SYMBOLS];
    int dot;
    char lookahead[MAX_SYMBOLS];
}Item;
typedef struct {
    Item items[MAX_STATES];
    int count;
}State;
State states[MAX_STATES];
int s_cnt = 0;
char non_terms[] = {'S', 'E', 'T', 'F'};
char terms[] = {'+', '-', '*', '/', '(', ')', 'n', '$'};
char FIRST[5][MAX_SYMBOLS] = {{0}};
char FOLLOW[5][MAX_SYMBOLS] = {{0}};
typedef struct {
    char type; // S: shift, R: reduce, A: accept
    int num; // 移入状态 / 产生式编号
} action;
action ACTION[MAX_STATES][8];
int GOTO[MAX_STATES][4] = {{0}};
const char* productions[] = {
    "S->E",
    "E->E+T",
    "E->E-T",
    "E->T",
    "T->T*F",
    "T->T/F",
    "T->F",
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
        for(int i=0; i<9; i++){
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
        for(int i=0; i<9; i++){
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

void add_item(State *state, char left, const char *right, int dot, const char *lookahead){
    for(int i=0; i<state->count; i++){
        // 项目已存在
        if(state->items[i].left == left && state->items[i].dot == dot && strcmp(state->items[i].right, right) == 0){
            for(int j=0; lookahead[j] != '\0'; j++){
                if(!strchr(state->items[i].lookahead, lookahead[j])){
                    int len = strlen(state->items[i].lookahead);
                    state->items[i].lookahead[len] = lookahead[j];
                    state->items[i].lookahead[len + 1] = '\0';
                }
            }
            return;
        }
    }
    state->items[state->count++] = (Item){left, {0}, dot, {0}};
    strcpy(state->items[state->count - 1].right, right);
    strcpy(state->items[state->count - 1].lookahead, lookahead);
}

int same_item(Item a, Item b){
    return a.left == b.left && a.dot == b.dot && strcmp(a.right, b.right) == 0 && strcmp(a.lookahead, b.lookahead) == 0;
}

int same_state(State a, State b){
    if(a.count != b.count)
        return 0;
    for(int i=0; i<a.count; i++){
        int found = 0;
        for(int j=0; j<b.count; j++){
            if(same_item(a.items[i], b.items[j])){
                found = 1;
                break;
            }
        }
        if(!found)
            return 0;
    }
    return 1;
}

void closure(State *set){
    int update = 1;
    while(update){
        update = 0;
        for(int i=0; i<set->count; i++){
            Item item = set->items[i];
            // .后是非终结符
            if(item.dot < strlen(item.right) && strchr(non_terms, item.right[item.dot])){
                char B = item.right[item.dot];
                for(int j=0; j<9; j++){
                    if(productions[j][0] == B){
                        char lookahead_set[MAX_SYMBOLS] = {0};
                        int lookahead_cnt = 0;
                        // 计算向前看符号
                        if(item.dot + 1 < strlen(item.right)){ 
                            char next_symbol = item.right[item.dot + 1];// 直接后续符号
                            if(strchr(terms, next_symbol))// 是终结符
                                lookahead_set[lookahead_cnt++] = next_symbol;
                            else{// 是非终结符
                                int n_index = strchr(non_terms, next_symbol) - non_terms;
                                for(int l=0; FIRST[n_index][l]!='\0'; l++){
                                    char sym = FIRST[n_index][l];
                                    if(sym != 'e')
                                        lookahead_set[lookahead_cnt++] = sym;
                                }
                                if(strchr(FIRST[n_index], 'e')){ // 包含空串
                                    for(int l=0; item.lookahead[l] != '\0'; l++)
                                        lookahead_set[lookahead_cnt++] = item.lookahead[l];
                                }
                            }
                        } 
                        else// 继承
                            for(int l=0; item.lookahead[l] != '\0'; l++)
                                lookahead_set[lookahead_cnt++] = item.lookahead[l];
                        // 添加
                        for(int k=0; k<lookahead_cnt; k++){
                            char lookahead[2] = {lookahead_set[k], '\0'};
                            int rec = set->count;
                            add_item(set, B, productions[j]+3, 0, lookahead);
                            if(set->count > rec)
                                update = 1;
                        }
                    }
                }
            }
        }
    }
}

void dfa(){
    states[0].count = 0;
    // S->.E, $
    add_item(&states[0], 'S', productions[0] + 3, 0, "$");
    closure(&states[0]);
    s_cnt = 1;
    int update = 1;
    while(update){
        update = 0;
        for(int i=0; i<s_cnt; i++){
            for(int k=0; k<states[i].count; k++){ // 遍历状态中的每个项目
                Item item = states[i].items[k];
                if(item.dot < strlen(item.right)){
                    State new_state;
                    new_state.count = 0;
                    char symbol = item.right[item.dot]; // .后的符号
                    for(int m=0; m<states[i].count; m++){
                        Item it = states[i].items[m];
                        if(it.dot < strlen(it.right) && it.right[it.dot] == symbol)
                            add_item(&new_state, it.left, it.right, it.dot+1, it.lookahead);
                    }
                    closure(&new_state);
                    int found = 0;// 检查新状态是否已存在
                    for(int n=0; n<s_cnt; n++){
                        if(same_state(states[n], new_state)){
                            if(strchr(terms, symbol)){// 对于终结符，更新ACTION
                                ACTION[i][strchr(terms, symbol) - terms].type = 'S';
                                ACTION[i][strchr(terms, symbol) - terms].num = n;
                            }
                            else// 对于非终结符，更新GOTO
                                GOTO[i][strchr(non_terms, symbol) - non_terms] = n;
                            found = 1;
                            break;
                        }
                    }
                    if(!found){
                        states[s_cnt] = new_state;
                        if(strchr(terms, symbol)){ // 对于终结符，更新ACTION
                            ACTION[i][strchr(terms, symbol) - terms].type = 'S';
                            ACTION[i][strchr(terms, symbol) - terms].num = s_cnt;
                        }
                        else // 对于非终结符，更新GOTO
                            GOTO[i][strchr(non_terms, symbol) - non_terms] = s_cnt;
                        s_cnt++;
                        update = 1;
                    }
                }
            }
        }
    }
}

void fill_tables(){
    // 拓广文法
    // 初始化
    memset(ACTION, 0, sizeof(ACTION));
    memset(GOTO, 0, sizeof(GOTO));
    
    dfa();
    for(int i=0; i<s_cnt; i++){
        for(int j=0; j<states[i].count; j++){
            Item item = states[i].items[j];
            if(item.dot >= strlen(item.right)){ // 规约项目
                if(item.left == 'S'){
                    ACTION[i][7].type = 'A';
                    ACTION[i][7].num = 0;
                }
                else{
                    for(int l = 0; item.lookahead[l] != '\0'; l++){
                        int index = strchr(terms, item.lookahead[l]) - terms;
                        ACTION[i][index].type = 'R';
                        for(int k = 0; k < 9; k++){
                            if(strcmp(productions[k] + 3, item.right) == 0 && productions[k][0] == item.left){
                                ACTION[i][index].num = k;
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
}

void print_tables(){
    printf("ACTION:\n");
    printf("state\t");
    for(int i = 0; i < 8; i++){
        printf("%c\t", terms[i]);
    }
    printf("\n");
    for(int i = 0; i < s_cnt; i++){
        printf("%d\t", i);
        for(int j = 0; j < sizeof(terms)/sizeof(terms[0]); j++){
            if(ACTION[i][j].type != 0){
                printf("%c%d\t", ACTION[i][j].type, ACTION[i][j].num);
            } else {
                printf(" \t");
            }
        }
        printf("\n");
    }

    printf("\nGOTO:\n");
    printf("state\t");
    for(int i = 0; i < 4; i++){
        printf("%c\t", non_terms[i]);
    }
    printf("\n");
    for(int i = 0; i < s_cnt; i++){
        printf("%d\t", i);
        for(int j = 0; j < sizeof(non_terms)/sizeof(non_terms[0]); j++){
            if(GOTO[i][j] != 0){
                printf("%d\t", GOTO[i][j]);
            } else {
                printf(" \t");
            }
        }
        printf("\n");
    }
}

void lr1analyze(char* expr){
    AnalysisStep steps;
    int top = 0; // 栈顶指针
    int ip = 0;  // 输入指针
    steps.stack[0] = '0';
    strcpy(steps.input, expr);
    strcat(steps.input, "$");

    do{
        int S = steps.stack[top] - '0'; // 栈顶状态
        char a = steps.input[ip];      // ip指向符号
        char *pos = strchr(terms, a);
        int index = pos - terms;

        if(ACTION[S][index].type == 'S'){ // 移入
            printf("shift\n");
            steps.stack[++top] = a;
            int next_state = ACTION[S][index].num;
            steps.stack[++top] = next_state + '0';
            ip++;
        } 
        else if(ACTION[S][index].type == 'R'){ // 规约
            int prod_index = ACTION[S][index].num;
            int prod_len = strlen(productions[prod_index] + 3);
            top -= 2 * prod_len; // 弹出2倍产生式右部长度的栈元素
            int T = steps.stack[top] - '0'; // 新的栈顶状态
            char non_term = productions[prod_index][0]; // 获取产生式左部非终结符
            steps.stack[++top] = non_term;
            steps.stack[++top] = GOTO[T][strchr(non_terms, non_term) - non_terms] + '0';
            printf("%d\n",prod_index);
        } 
        else if(ACTION[S][index].type == 'A'){ // 接受
            printf("accept\n");
            return;
        }
        else{
            printf("error\n");
            return;
        }
    }while(1);
}

int main(){
    first();
    follow();
    fill_tables();
    // print_tables();
    char expr[100];
    scanf("%99s", expr);
    lr1analyze(expr);
    return 0;
}