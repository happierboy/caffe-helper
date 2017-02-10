#include <iostream>
#include <string>
#include <map>

using namespace std;
int main(){

map<string, string> mapStudent;
map<string, string>::iterator iter;

mapStudent.insert(pair<string, string>("zhangli", "0"));
mapStudent["feijing"] = "1";
mapStudent["kangkang"] = "2";
iter = mapStudent.find("zhangli");
if(iter!=mapStudent.end())
	cout<<"find it"<<endl;
else
	cout<<"do not find it"<<endl;

return 0;
}
