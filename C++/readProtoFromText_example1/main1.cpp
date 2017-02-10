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

/*
int main(){
std::map<std::string, int> name_to_label;
const string label_map_file = "labelmap_voc.prototxt";
LabelMap label_map;
ReadProtoFromTextFile(label_map_file, &label_map);
MapNameToLabel(label_map, check_label, &name_to_label);
while(infile >> filename >> labelname)
	lines.push_back(std::make_pair(filename, labelname));
}
*/
int main()
{
    SolverParameter SGD;

    if(!ReadProtoFromTextFile("solver.prototxt", &SGD))
    {
       cout<<"error opening file"<<endl; 
       return -1;
    }

    cout<<"hello,world"<<endl;
    cout<<SGD.train_net()<<endl;
    cout<<SGD.base_lr()<<endl;
    cout<<SGD.lr_policy()<<endl;

    NetParameter VGG16;
    if(!ReadProtoFromTextFile("train.prototxt", &VGG16))
    {
       cout<<"error opening file"<<endl; 
       return -1;
    }
    cout<<VGG16.name()<<endl;
    cout<<VGG16.name().data()<<"\t"<<VGG16.name().length()<<endl;
    cout<<VGG16.layer_size()<<endl;
    cout<<VGG16.layer(0).name()<<endl;
    cout<<VGG16.layer(1).name()<<endl;
    return 0;
}
