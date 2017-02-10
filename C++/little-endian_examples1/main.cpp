#include <stdio.h>

int main(){
int num = 1;
if(*(char*)&num == 1)
	printf("this is a little endian\n");
else
	printf("this is a big endian\n");
return 0;
}
