#include "test.pb.h"
#include <unistd.h>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <fcntl.h>
#include <google/protobuf/text_format.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/text_format.h>
using namespace std;
using google::protobuf::io::FileInputStream;
using google::protobuf::io::FileOutputStream;

int main(){
	manager a;
	int fd = open("in.txt", O_RDONLY);
	FileInputStream* input = new FileInputStream(fd);
  	bool success = google::protobuf::TextFormat::Parse(input, &a);
	cout<<a.t1().name()<<endl;	
	cout<<"top size: "<<a.t1().top_size()<<"\t"<<a.t1().top(0)<<"\t"<<a.t1().top(1)<<endl;
	cout<<a.t1().bottom()<<endl;
	cout<<a.t1().phase()<<endl;
	cout<<a.manager_name()<<endl;
	delete input;
	close(fd);
	return 0;
}
