#include "frequency_monitoring/frequency_point.hpp"

namespace frequency_monitoring
{
FrequencyPoint::FrequencyPoint() : mean{-1}, min{-1}, max{-1}, sd{-1}
{
}

FrequencyPoint::FrequencyPoint(const std::vector<double>& timestamps)
{
    // tmp vector for calculation
    std::vector<double> frequencies(timestamps.size());

    // transform to vector of frequencies
    double size = static_cast<double>(timestamps.size());
    auto get_frequency = [](double t2, double t1) -> double {
        return 1. / (t2 - t1);
    };
    std::transform(timestamps.begin() + 1,
                   timestamps.end(),
                   timestamps.begin(),
                   std::back_inserter(frequencies),
                   get_frequency);

    // computing mean of frequencies
    mean = (frequencies[size - 1] - frequencies[0]) / size;

    // computing min and max frequencies
    min = *std::min_element(frequencies.begin(), frequencies.end());
    max = *std::max_element(frequencies.begin(), frequencies.end());

    // computing standard deviation
    double mean_ = mean;  // for capture below
    auto get_variance = [&mean_, &size](double accumulator,
                                        const double& value) -> double {
        double dmean = (value - mean_) * (value - mean_);
        return accumulator + (dmean / (size - 1));
    };
    double variance = std::accumulate(
        frequencies.begin(), frequencies.end(), 0.0, get_variance);
    sd = sqrt(variance);
}

}  // namespace frequency_monitoring
