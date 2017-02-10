#include "boost/scoped_ptr.hpp"
#include <string>
#include <iostream>
using namespace std;
int main() {
  {
  boost::scoped_ptr<std::string> p(new std::string("Use scoped_ptr often."));
  //boost::scoped_ptr<std::string> another_p = p;
  if (p)
    std::cout << *p << std::endl;
    
  // 获取字符串的大小
  size_t i=p->size();

  // 给字符串赋新值
  *p="Acts just like a pointer";
  if (p)
    std::cout << *p << std::endl;  

  } // 这里p被销毁，并删除std::string
}
