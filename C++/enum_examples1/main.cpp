#include <stdio.h>

int main(){
enum Animal{
	animal0 = 1,
	animal1 = 2,
	animal2,
	animal3,
    };
Animal x1 = animal0;
Animal x2 = animal3;
printf("%x\n", &x1); 
printf("%x\n", &x2);
return 0;
}
