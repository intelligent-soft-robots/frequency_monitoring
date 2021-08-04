#include "frequency_monitoring/frequency_point.hpp"

namespace frequency_monitoring
{
FrequencyPoint::FrequencyPoint() : mean{-1}, min{-1}, max{-1}, sd{-1}
{
}

void FrequencyPoint::set(const std::vector<double>& timestamps)
{

  frequencies_.resize(timestamps.size());
  frequencies_.clear();
    
    // transform to vector of frequencies
    double size = static_cast<double>(timestamps.size());
    auto get_frequency = [](double t2, double t1) -> double {
        return 1. / (t2 - t1);
    };
    std::transform(timestamps.begin() + 1,
                   timestamps.end(),
                   timestamps.begin(),
                   std::back_inserter(frequencies_),
                   get_frequency);

    // computing mean of frequencies
    mean = size / (timestamps[size - 1] - timestamps[0]);
    
    // computing min and max frequencies
    min = *std::min_element(frequencies_.begin(), frequencies_.end());
    max = *std::max_element(frequencies_.begin(), frequencies_.end());

    // computing standard deviation
    double mean_ = mean;  // for capture below
    auto get_variance = [&mean_, &size](double accumulator,
                                        const double& value) -> double {
        double dmean = (value - mean_) * (value - mean_);
        return accumulator + dmean;
    };
    double variance = std::accumulate(
        frequencies_.begin(), frequencies_.end(), 0.0, get_variance);
    variance/=(size-1);
    sd = sqrt(variance);
}

}  // namespace frequency_monitoring
