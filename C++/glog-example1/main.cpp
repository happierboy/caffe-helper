#include <iostream>
#include <glog/logging.h>

using namespace std;
int main(int argc, char**argv){
//google::ParseCommandLineFlags(&argc, &argv, true);  
google::InitGoogleLogging(argv[0]);  
//FLAGS_log_dir=".";
LOG(INFO)<<"hello glog";
return 0;
}
