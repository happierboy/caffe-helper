#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <string>
#include <set>
#include <exception>
#include <iostream>

struct debug_settings
{
    std::string m_file;               // log filename
    int m_level;                      // debug level
    std::set<std::string> m_modules;  // modules where logging is enabled
    void load(const std::string &filename);
    void save(const std::string &filename);
};

void debug_settings::load(const std::string &filename)
{

    // Create empty property tree object
    using boost::property_tree::ptree;
    ptree pt;
    read_xml(filename, pt);
    m_file = pt.get<std::string>("debug.filename");
    m_level = pt.get("debug.level", 0);
    BOOST_FOREACH(ptree::value_type &v, pt.get_child("debug.modules")){
         m_modules.insert(v.second.data());
    }
    for(std::set<std::string>::iterator iter = m_modules.begin(); iter!=m_modules.end();iter++)
	std::cout<<*iter<<std::endl;

}

void debug_settings::save(const std::string &filename)
{
    using boost::property_tree::ptree;
    ptree pt;
    pt.put("debug.filename", m_file);
    pt.put("debug.level", m_level);
    /*BOOST_FOREACH(const std::string &name, m_modules)
        pt.put("debug.modules.module", std::string("zhangli")+name, true);*/
    write_xml(filename, pt);
}

int main()
{
    try
    {
        debug_settings ds;
        ds.load("debug_settings.xml");
        ds.save("debug_settings_out.xml");
        std::cout << "Success\n";
    }
    catch (std::exception &e)
    {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
