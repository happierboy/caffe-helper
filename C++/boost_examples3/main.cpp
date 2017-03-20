#include <boost/algorithm/string.hpp>
#include <string>
#include <boost/shared_ptr.hpp>
#include <vector>
#include <iostream>
using namespace std;
int main(){
boost::shared_ptr<string> a_p(new string("1,2,3"));
cout<<*a_p<<endl;
return 0;
}
