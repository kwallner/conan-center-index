#include <cpptoml.h>
#include <iostream>

int main(int argc, char* argv[])
{
    std::shared_ptr<cpptoml::table> root = cpptoml::make_table();
    root->insert("Name", std::string("cpptoml"));
    root->insert("Version", 0.1);

    std::cout << (*root);
    return 0;
}