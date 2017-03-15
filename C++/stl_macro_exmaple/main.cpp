#include <stdio.h>
#include <iostream>
#include <string>
#include <map>
using namespace std;

// A simple registry for caffe commands.
typedef int (*BrewFunction)();
typedef map<string, BrewFunction> BrewMap;
BrewMap g_brew_map;


#define RegisterBrewFunction(func) \
class __Registerer_##func { \
 public: /* NOLINT */ \
  __Registerer_##func() { \
    g_brew_map[#func] = &func; \
  } \
}; \
__Registerer_##func g_registerer_##func; \



static BrewFunction GetBrewFunction(const string& name) {
  if (g_brew_map.count(name)) {
    return g_brew_map[name];
  }
}

int train(){
	cout << "hello world" << endl;
	return 0;
}
int main(){
RegisterBrewFunction(train);
return GetBrewFunction(string("train"))();
}
