#include "iceoryx_posh/popo/typed_subscriber.hpp"
#include "iceoryx_posh/runtime/posh_runtime.hpp"

#include <chrono>
#include <iostream>

struct DummyContent
{
    uint32_t counter;
    uint32_t id;
};

void receive()
{
    iox::popo::TypedSubscriber<DummyContent> subscriber({"Group", "Instance", "Counter"});

    subscriber.subscribe();

    // Thats enough for the compile test
    
    subscriber.unsubscribe();
}

int dummy()
{
    iox::runtime::PoshRuntime::initRuntime("iox-subscriber");

    std::thread receiver(receive);
    receiver.join();

    return (EXIT_SUCCESS);
}

int main()
{
    std::cout << "Dummy Test" << std::endl;
    return (EXIT_SUCCESS);
}
