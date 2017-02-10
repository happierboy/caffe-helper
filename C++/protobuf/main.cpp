#include "test.pb.h"
#include <stdio.h>
#include <string>
using namespace std;
int main(){
Book book;
book.set_money(150);
int size = book.ByteSize();
unsigned char bts[size];
book.SerializeToArray(bts, size);
for(int i = 0; i<size;i++)
	printf("0x%x\n", bts[i]);

book.set_money(100);
book.ParseFromArray(bts, size);
printf("%d\n", book.money());
return 0;
}
