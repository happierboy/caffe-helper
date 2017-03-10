#include <stdio.h>
#include <iostream>
using namespace std;

#define RegisterBrewFunction(func) \
namespace{\
class __Registerer_##func{
public:\
__Registerer_##func(){\
g_brew_map[#func] = &func;\
}\
};\
_Registerer_##func g_registerer_##func;
}

int train(){
cout << "hello world" << endl;
return 0;
}
int main(){
RegistererBrewFunction(train);
}
