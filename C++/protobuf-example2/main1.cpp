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
	manager* a = new manager();
	a->mutable_t1()->set_name("zhangli");
	a->mutable_t1()->set_type(10);
	a->mutable_t1()->add_top(10);
	a->mutable_t1()->add_top(11);
	a->mutable_t1()->set_bottom(10);
	a->mutable_t1()->set_phase(10);
	a->set_manager_name("zhangli");
	int fd = open("out.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
	FileOutputStream* output = new FileOutputStream(fd);
  	bool success = google::protobuf::TextFormat::Print(*a, output);
	std::cout<<success<<std::endl;
	delete output;
	close(fd);
	return 0;
}
