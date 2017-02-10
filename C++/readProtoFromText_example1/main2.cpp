#include <fcntl.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
#include <utility>
#include <vector>
#include <google/protobuf/text_format.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/io/coded_stream.h>
#include "caffe.pb.h"

using namespace caffe;
using namespace std;

using google::protobuf::io::FileInputStream;
using google::protobuf::Message;

bool ReadProtoFromTextFile(const char* filename, Message* proto) {
  int fd = open(filename, O_RDONLY);//打开文件
  FileInputStream* input = new FileInputStream(fd);//新建一个FileInputStream对象 input
  bool success = google::protobuf::TextFormat::Parse(input, proto);
  //解析input文件中的Message， 即使文件中参数定义顺序与Message中的参数定义顺序不一致，也可以解析。
  delete input;
  close(fd);
  return success;
}

bool MapNameToLabel(const LabelMap& map, const bool strict_check,
    std::map<string, int>* name_to_label) {
  // cleanup
  name_to_label->clear();

  for (int i = 0; i < map.item_size(); ++i) {
    const string& name = map.item(i).name();
    const int label = map.item(i).label();
    if (strict_check) {
      if (!name_to_label->insert(std::make_pair(name, label)).second) {
        return false;
      }
    } else {
      (*name_to_label)[name] = label;
    }
  }
  return true;
}


int main(){
	std::map<std::string, int> name_to_label;
	const string label_map_file = "labelmap_voc.prototxt";
	LabelMap label_map;
	ReadProtoFromTextFile(label_map_file.c_str(), &label_map);
	cout<<"==============================="<<endl;
	cout<<"==item info"<<endl;
	cout<<"==============================="<<endl;
	cout<<"item size\t"<<label_map.item_size()<<"\tfirst element:\t"<<label_map.item(0).name()<<"\t"<<label_map.item(0).display_name()<<endl;
	MapNameToLabel(label_map, true, &name_to_label);

	cout<<"==============================="<<endl;
	cout<<"==test before insertion"<<endl;
	cout<<"==============================="<<endl;
	std::map<string, int>::iterator _iter = name_to_label.find("hello world");
	if(_iter != name_to_label.end()){
		std::cout<<"find the above"<<std::endl;
	}
	else{
		std::cout<<"cannot find the above"<<std::endl;
	}

	cout<<"==============================="<<endl;
	cout<<"==test after insertion"<<endl;
	cout<<"==============================="<<endl;
	name_to_label.insert(std::make_pair("hello world", 100));
	name_to_label.insert(std::map<string, int>::value_type("hello world value_type", 100));
	_iter = name_to_label.find("hello world");
	if(_iter != name_to_label.end()){
		std::cout<<"find the above"<<std::endl;
	}
	else{
		std::cout<<"cannot find the above"<<std::endl;
	}

	cout<<"==============================="<<endl;
	cout<<"==visit all elements"<<endl;
	cout<<"==============================="<<endl;
	cout<<"element size\t"<<name_to_label.size()<<endl;
	for(_iter = name_to_label.begin(); _iter!=name_to_label.end();++_iter){
		std::cout<<_iter->first<< "\t"<<_iter->second<<std::endl;
	}

	cout<<"==============================="<<endl;
	cout<<"==test erase element"<<endl;
	cout<<"==============================="<<endl;
	name_to_label.erase(name_to_label.find("hello world value_type"));
	cout<<"==============================="<<endl;
	cout<<"==after clearing"<<endl;
	cout<<"==============================="<<endl;
	name_to_label.clear();
	for(_iter = name_to_label.begin(); _iter!=name_to_label.end();++_iter){
		std::cout<<_iter->first<< "\t"<<_iter->second<<std::endl;
	}
	return 0;
}

