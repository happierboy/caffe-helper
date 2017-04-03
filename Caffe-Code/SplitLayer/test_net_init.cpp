    #include <cstring>
    #include <cstdio>
    #include <cstdlib>
    #include <string>
    #include <utility>
    #include <vector>
    #include <iostream>
    #include "caffe/common.hpp"
    #include "caffe/net.hpp"
    #include "caffe/util/insert_splits.hpp"
    #include "caffe/util/upgrade_proto.hpp"
    #include "caffe/util/io.hpp"

    using namespace caffe;

    int main(int argc, char **argv)
    {
        if(argc!=3)
        {
            printf("./test_net_init net_proto_file net_out_proto_file\n");
            return 0;
        }

        string proto_filename=string(argv[1]);
	    string proto_outname = string(argv[2]);

        NetParameter param1;
        caffe::ReadNetParamsFromTextFileOrDie(proto_filename, &param1);
        printf("params before InsertSplits():\n");
        for(int layer_id=0;layer_id<param1.layer_size();layer_id++)
        {
            const LayerParameter& layer_param = param1.layer(layer_id);
            printf("%d: %s\n",layer_id, layer_param.name().c_str());
        }

        //do InsertSplits
        NetParameter param2;
        caffe::InsertSplits(param1, &param2);

        printf("\nparams after InsertSplits():\n");
        for(int layer_id=0;layer_id<param2.layer_size();layer_id++)
        {
            const LayerParameter& layer_param = param2.layer(layer_id);
            printf("%d: %s\n",layer_id, layer_param.name().c_str());
        }
	    caffe::WriteProtoToTextFile(param2, proto_outname.c_str());
        return 0;
    }
