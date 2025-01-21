#include <stdio.h>
#include <iostream>
#include <string>
#include <fstream>
#include <unordered_set>

using namespace std;

int state = 0; // 状态
int line_cnt = 1; // 行计数器
int inComment = 0; // 在注释中
int KW_cnt=0, ID_cnt=0, OP_cnt=0, DL_cnt=0, CH_cnt=0, STR_cnt=0, NUM_cnt=0; // 关键字、标识符、运算符、分隔符、字符常量、字符串、数值常量计数器
int error_cnt = 0; // 词法错误计数器

unordered_set<string> KWs = {"auto", "double", "int", "struct", "break", "else", "static", "long", "switch", "case", "enum", "register", "typedef", "char", "extern", "return", "union", "const", "float", "short", "unsigned", "continue", "for", "signed", "void", "default", "goto", "sizeof", "volatile", "do", "if", "while"};
unordered_set<string> OPs = {"+", "-", "*", "/", "%", "++", "--", "==", "!=", ">", "<", ">=", "<=", "&&", "||", "!",
"&", "|", "^", "~", "<<", ">>", "=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|=", ".", "->"};

bool isKeyword(string &s)
{
  return KWs.find(s) != KWs.end();
}

bool isOperator(string &s)
{
  return OPs.find(s) != OPs.end();
}

bool isDelimiter(char c)
{
  return c==';' || c==',' || c==':' || c=='?' || c=='(' || c==')' || c=='[' || c==']' || c=='{' || c=='}';
}

bool isLetter(char c)
{
  return isalpha(c) || c=='_';
}

int main(int argc, char* argv[])
{
    ifstream file("test.c");
    
    char c;
    string word;

    while(file.get(c)){
      if(inComment!=0){
        if(c=='\n'){
          line_cnt++;
          if(inComment==1)
            inComment = 0;
        }
        if(inComment==2 && c=='*' && file.peek()=='/'){
          file.get(c);
          inComment = 0;
        }
        continue;
      }

      if(c=='\n' && state==0)
        line_cnt++;
        
      if(state!=8 && state!=9){
        if(c=='/' && file.peek()=='/'){
          file.get(c);
          inComment = 1;
          continue;
        }
        if(c=='/' && file.peek()=='*'){
          file.get(c);
          inComment = 2;
          continue;
        }
        if(c=='@'){// 注释中和引号里的@合法
          cout << line_cnt << " <ERROR,@>" << endl;
          error_cnt++;
          continue;
        }
      }

      switch(state){
        case 0:
          if(c=='L' || c=='u' || c=='U' || (c=='u'&&file.peek()=='8')){
            word += c;
            if(c=='u' && file.peek()=='8')
              word += file.get();
            if(file.peek()=='\"'){
              word += file.get();
              state = 9;
            }
            else if(file.peek()=='\''){
              word += file.get();
              state = 8;
            }
            else
              state = 1;
          }
          else if(isLetter(c)){
            word += c;
            state = 1;
          }
          else if(isdigit(c)){
            word += c;
            state = 2;
          }
          else if(c=='.' && isdigit(file.peek())){// 浮点
            word += c;
            state = 3;
          }
          else if(isDelimiter(c)){
            cout << line_cnt <<" <DELIMITER," << c << ">" << endl;
            DL_cnt++;
          }
          else if(c=='\''){
            word += c;
            state = 8;
          }
          else if(c=='\"'){
            word += c;
            state = 9;
          }
          else if(!isspace(c)){
            word += c;
            state = 10;
          }
          break;
        case 1:
          if(isLetter(c) || isdigit(c)){
            word += c;
          }
          else{
            if(isKeyword(word)){
              cout << line_cnt << " <KEYWORD," << word << ">" << endl;
              KW_cnt++;
            }
            else{
              cout << line_cnt << " <IDENTIFIER," << word << ">" << endl;
              ID_cnt++;
            }
            word.clear();
            state = 0;
            file.unget();// 退回
          }
          break;
        case 2:// 数值判断start
          if(isdigit(c)){
            word += c;
            if(word[0]=='0' && c>='8'){// 非法8进制
              cout << line_cnt << " <ERROR," << word << ">" << endl;
              error_cnt++;
              word.clear();
              state = 0;
            }
          }
          else if(c=='.'){
            word += c;
            state = 3;
          }
          else if(c=='x' || c=='X'){
            if(word=="0"){
              word += c;
              state = 11;
            }
            else{
              cout << line_cnt << " <ERROR," << word << c << ">" << endl;
              error_cnt++;
              word.clear();
              state = 0;
            }
          }
          else if(c=='E' || c=='e'){
            word += c;
            state = 5;
          }
          else if(c=='U' || c=='u' || c=='L' || c=='l'){
            word += c;
            state = 12;
          }
          else if(isLetter(c)){// 非法标识符
            cout << line_cnt << " <ERROR," << word << c << ">" << endl;
            error_cnt++;
            word.clear();
            state = 0;
          }
          else{
            cout << line_cnt << " <NUMBER," << word << ">" << endl;
            NUM_cnt++;
            word.clear();
            state = 0;
            file.unget();
          }
          break;
        case 3:
          if(isdigit(c)){
            word += c;
            state = 4;
          }
          break;
        case 4:
          if(isdigit(c)){
            word += c;
          }
          else if(c=='E' || c=='e'){
            word += c;
            state = 5;
          }
          else if(c=='f' || c=='F' || c=='l' || c=='L'){// 浮点后缀
            word += c;
            cout << line_cnt << " <NUMBER," << word << ">" << endl;
            NUM_cnt++;
            word.clear();
            state = 0;
          }
          else{
            cout << line_cnt << " <NUMBER," << word << ">" << endl;
            NUM_cnt++;
            word.clear();
            state = 0;
            file.unget();
          }
          break;
        case 5:
          if(c=='+' || c=='-'){
            word += c;
            state = 6;
          }
          else if(isdigit(c)){
            word += c;
            state = 7;
          }
          else{// 非法标识符(1e)
            file.unget();
            cout << line_cnt << " <ERROR," << word << ">" << endl;
            error_cnt++;
            word.clear();
            state = 0;
          }
          break;
        case 6:
          if(isdigit(c)){
            word += c;
            state = 7;
          }
          break;
        case 7:// 数值判断end
          if(isdigit(c)){
            word += c;
          }
          else if(c=='f' || c=='F' || c=='l' || c=='L'){
            word += c;
            cout << line_cnt << " <NUMBER," << word << ">" << endl;
            NUM_cnt++;
            word.clear();
            state = 0;
          }
          else{
            cout << line_cnt << " <NUMBER," << word << ">" << endl;
            NUM_cnt++;
            word.clear();
            state = 0;
            file.unget();
          }
          break;
        case 8:// 字符常量
          word += c;
          if(c=='\\'){// 转义字符
            if(file.peek()=='\'' || file.peek()=='\\'){
              word += file.get();
            }
          }
          else if(c=='\''){
            cout << line_cnt << " <CHARCON," << word << ">" << endl;
            CH_cnt++;
            word.clear();
            state = 0;
          }
          else if(c=='\n'){// 未闭合
            word.pop_back();
            cout << line_cnt << " <ERROR," << word << ">" << endl;
            error_cnt++;
            word.clear();
            line_cnt++;
            state = 0;
          }
          break;
        case 9:// 字符串
          word += c;
          if(c=='\\'){// 转义字符
            if(file.peek()=='\"' || file.peek()=='\\'){
              word += file.get();
            }
          }
          else if(c=='\"'){
            cout << line_cnt << " <STRING," << word << ">" << endl;
            STR_cnt++;
            word.clear();
            state = 0;
          }
          else if(c=='\n'){// 未闭合
            word.pop_back();
            cout << line_cnt << " <ERROR," << word << ">" << endl;
            error_cnt++;
            word.clear();
            line_cnt++;
            state = 0;
          }
          break;
        case 10:// 运算符
            word += c;
            if(word.size()==3){
              string str0 = word.substr(0, 1);
              string str1 = word.substr(0, 2);
              if(isOperator(word)){// 3
                cout << line_cnt << " <OPERATOR," << word << ">" << endl;
                OP_cnt++;
                word.clear();
                state = 0;
              }
              else if(isOperator(str1)){// 2
                cout << line_cnt << " <OPERATOR," << str1 << ">" << endl;
                OP_cnt++;
                file.unget();
                word.clear();
                state = 0;
              }
              else if(isOperator(str0)){// 1
                cout << line_cnt << " <OPERATOR," << str0 << ">" << endl;
                OP_cnt++;
                file.unget();
                file.unget();
                word.clear();
                state = 0;
              }
            }
            else{
              if(isOperator(word)){
                if(word.size()==2 && file.peek()!=EOF)
                  continue;
                cout << line_cnt << " <OPERATOR," << word << ">" << endl;
                OP_cnt++;
                word.clear();
                state = 0;
              }
            }
          break;
        case 11:// 16进制
          if(isdigit(c) || (c>='A'&&c<='F') || (c>='a'&&c<='f')){
            word += c;
          }
          else{
            if(word.length()>2){
              cout << line_cnt << " <NUMBER," << word << ">" << endl;
              NUM_cnt++;
            }
            else{
              cout << line_cnt << " <ERROR," << word << c << ">" << endl;
              error_cnt++;
            }
            word.clear();
            state = 0;
            file.unget();
          }
          break;
        case 12:// 整数后缀U/UL/ULL/L/LL//LLU
          if(c=='U' || c=='u'){
            if(word.back()=='U' || word.back()=='u'){
              cout << line_cnt << " <ERROR," << word << c << ">" << endl;
              error_cnt++;
              word.clear();
              state = 0;
            }
            else
              word += c;
          }
          else if(c=='L' || c=='l'){
            word += c;
          }
          else if(isLetter(c)){// 非法标识符
            cout << line_cnt << " <ERROR," << word << c << ">" << endl;
            error_cnt++;
            word.clear();
            state = 0;
          }
          else{
            cout << line_cnt << " <NUMBER," << word << ">" << endl;
            NUM_cnt++;
            word.clear();
            state = 0;
            file.unget();
          }
          break;
      }
    }
    if(!word.empty()){// 到EOF未结束的
      if(isKeyword(word)){
        cout << line_cnt << " <KEYWORD," << word << ">" << endl;
        KW_cnt++;
      }
      else if(state==2 || state==4 || state==7 || state==11 || state==12){
        cout << line_cnt << " <NUMBER," << word << ">" << endl;
        NUM_cnt++;
      }
      else{
        cout << line_cnt << " <IDENTIFIER," << word << ">" << endl;
        ID_cnt++;
      }
      word.clear();
    }

    file.close();

    cout << line_cnt << endl;
    cout << KW_cnt << " " << ID_cnt << " " << OP_cnt << " " << DL_cnt << " " << CH_cnt << " " << STR_cnt << " " << NUM_cnt << endl;
    cout << error_cnt << endl;

    return 0;
}