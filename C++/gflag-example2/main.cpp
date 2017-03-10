#include <iostream>
#include <stdio.h>
#include <gflags/gflags.h>  
bool ValidatePort(const char* flagname, int32_t value);

DECLARE_int32(port);  
DEFINE_int32(port, 0, "What port to listen on");  
DEFINE_bool(big_menu, true, "Include 'advanced' options in the menu listing");
DEFINE_string(languages, "english, french, german", "comma-seperated list of languages to offer in the 'lang' menu");

bool ValidatePort(const char* flagname, int32_t value) {  
    if (value > 0 && value<32768)   // value is ok  
        return true;  
    printf("Invalid value for --%s: %d\n", flagname, (int)value);  
    return false;  
}

int main(int argc,char*argv[])  
{  
    std::string usage("This program does nothing.  Sample usage:\n");  
    usage += std::string(argv[0])+" --port 1234 \n or :\n -flagfile=foo.conf";  
  
    google::SetUsageMessage(usage);  
    bool port_dummy = google::RegisterFlagValidator(&FLAGS_port,&ValidatePort);  
    google::ParseCommandLineFlags(&argc,&argv,true);  
  
    std::cout<<"port :"<< FLAGS_port<< std::endl;  
  
    return 0;  
}