#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <string>
#include <set>
#include <exception>
#include <iostream>

void load_xml(const std::string &filename)
{

    // Create empty property tree object
    using boost::property_tree::ptree;
    ptree pt;
    read_xml(filename, pt);

    int height = pt.get<int>("annotation.size.height");
    int width = pt.get<int>("annotation.size.width");

    BOOST_FOREACH(ptree::value_type &v1, pt.get_child("annotation")){
        if (v1.first == "object") {
            ptree object = v1.second;
            BOOST_FOREACH(ptree::value_type &v2, object.get_child("")){
                ptree pt2 = v2.second;
                if(v2.first=="name"){
                    std::string name = pt2.data();
                    std::cout<<name<<std::endl;
                }
                if(v2.first=="bndbox"){
                    int xmin = pt2.get("xmin", 0);
                    int ymin = pt2.get("ymin", 0);
                    int xmax = pt2.get("xmax", 0);
                    int ymax = pt2.get("ymax", 0);
                    std::cout<<xmin<<"\t"<<xmax<<"\t"<<ymin<<"\t"<<ymax<<std::endl;
                }
            }
        }
    }
}

int main()
{
    try
    {
        load_xml("000001.xml");
        std::cout << "Success\n";
    }
    catch (std::exception &e)
    {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
