#include <algorithm>
#include <string>
#include <iostream>
#include <memory>
using namespace std;

int main(){
	std::shared_ptr<int> sp;
	sp.reset(new int);
	*sp = 10;
	std::cout<<*sp<<std::endl;

	sp.reset(new int); //delete managed object, acquires new pointer;
	*sp = 20;
	std::cout<<*sp<<std::endl;
	
	sp.reset();
	return 0;
}
