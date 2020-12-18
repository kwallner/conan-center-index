#include "mosquittopp.h"

int main(int argc, char *argv[])
{
    mosqpp::lib_init();
    mosqpp::lib_cleanup();

    return 0;
}