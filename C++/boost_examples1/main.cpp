#include <boost/filesystem.hpp>
#include <iostream>

int main(){
boost::filesystem::path p("/home/mozat/Desktop/photo.jgp");
std::cout<<p.stem()<<std::endl;
std::cout<<p.extension()<<std::endl;
return 0;
}
