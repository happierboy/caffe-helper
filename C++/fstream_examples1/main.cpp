#include <fstream>
#include <string>
#include <iostream>

using namespace std;

int main(){
    string filename = "1.jpg";
    fstream file(filename.c_str(), ios::in|ios::binary|ios::ate);
    int size = file.tellg();
    cout<<size<<endl;
    return 0;
}
