#include <string>
#include <iostream>
class A{
public:
explicit A(){
std::cout<<"A"<<std::endl;
}
};
class B: public A{
public:
explicit B(){
std::cout<<"B"<<std::endl;
}
};

int main(){
B b = B();
return 0;
}
