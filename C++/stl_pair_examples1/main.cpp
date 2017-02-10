#include <iostream>
#include <utility>
#include <string>

using namespace std;

int main(){
pair<string, double> product1("kangkang", 3);
pair<string, double> product2, product3;

product2.first = "zhangli";
product2.second = 1;

product3 = make_pair("feijing", 2);
cout<<product1.first<<endl;
cout<<product2.first<<endl;
cout<<product3.first<<endl;

/*
pair<string, string, double) product4;
product4.first = "xinru";
product4.second = "brother";
product4.third = 4;

cout<<product4.third<<endl;
*/
return 0;
}
