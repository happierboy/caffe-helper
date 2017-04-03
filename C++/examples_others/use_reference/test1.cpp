#include <vector>
#include <iostream>

using namespace std;

void callVector(vector<int> t1){
	cout<<&(t1)<<endl;
	cout<<t1[0]<<endl;
	cout<<t1[1]<<endl;
	t1[0] = 2;
}

int main(){
	vector<int> t1;
	t1.resize(4);
	t1[0]=1;
	cout<<&(t1)<<endl;
	callVector(t1);
	cout<<t1[0]<<endl;
	cout<<t1[1]<<endl;
	return 0;
}
