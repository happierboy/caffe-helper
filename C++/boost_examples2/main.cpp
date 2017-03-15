#include <boost/algorithm/string.hpp>
#include <string>
#include <vector>
#include <iostream>
using namespace std;
int main(){
string a = "1,2,3";
vector<string> strings;
boost::split(strings, a, boost::is_any_of(","));
for(int i = 0;i<strings.size();i++){
	cout<<strings[i]<<endl;
}
return 0;
}
