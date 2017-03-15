#include <stdio.h>
#include <string>
#define Connect(x,y)       x##y
//#define ToChar(x)          #(@x)
#define ToString(x)        #x
#define TOA(x)     b##x##AA
int main(){
	//char a = ToChar(a);
	//printf("ToChar(a), %c\n", a);
	std::string str = ToString(123);
	printf("ToString(123), %s\n", str.c_str());
	int Connect(x,y) = 10;
	printf("Connect(x,y), %d, xy, %d\n", Connect(x,y), xy);
	int TOA(X) = 10;
	printf("TOA(X), %d, bXAA, %d\n", TOA(X), bXAA);
	return 0;
}
