#include <iostream>
#include <stdio.h>
#define AXX2(x) #x
#define AXX3(x) AXX3_##x
using namespace std;
int main(){
	cout<<AXX2(2)<<endl;
	int AXX3(3) = 100;
	cout<<AXX3(3)<<"AXX3(3)"<<endl;
	return 0;
}
