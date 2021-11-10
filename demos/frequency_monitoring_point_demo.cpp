#include "frequency_monitoring/frequency_point.hpp"

void execute()
{
    double period = 0.1;
    double value = 0;
    bool plus = false;
    std::vector<double> timestamps;

    for (int i = 0; i < 100; i++)
    {
        timestamps.push_back(value);
        if (plus)
        {
            value += period + 0.01;
        }
        else
        {
            value += period - 0.01;
        }
        plus = !plus;
    }

    frequency_monitoring::FrequencyPoint fp;
    fp.set(timestamps);

    std::cout << "mean:" << fp.mean << std::endl;
    std::cout << "sd:" << fp.sd << std::endl;
    std::cout << "min:" << fp.min << std::endl;
    std::cout << "max:" << fp.max << std::endl;
}

int main()
{
    execute();
}
