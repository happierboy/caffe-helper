#include <stdio.h>
#include <iostream>
#include "caffe/proto/caffe.pb.h"
#include "caffe/util/db.hpp"
#include "caffe/util/format.hpp"
#include "caffe/util/io.hpp"
#include "caffe/util/rng.hpp"

using namespace caffe;
using namespace std;

int main(){
int line_id = 10;
string key_str = format_int(line_id, 8) + "_.line";
cout<<key_str<<endl;
return 0;
}
