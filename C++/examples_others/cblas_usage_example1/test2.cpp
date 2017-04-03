#include <cmath>
#include <cblas.h>
#include <iostream>

using namespace std;

int main(){
float a[5] = {1,1,1,1,1};
float b[5] = {2,3,2,2,2};
int n = 2;
float c = cblas_sdot(n, a, 1, b, 1);
cout << c <<endl;
return 0;
}

