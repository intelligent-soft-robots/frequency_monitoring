#pragma once

#include <math.h>
#include <algorithm>
#include <numeric>

namespace frequency_monitoring
{
/*! An instance of FrequencyPoint encapsulates
 *  a minimal value, a maximal value, a mean and
 *  a standard deviation
 */
class FrequencyPoint
{
public:
    /* ! Construct an instance of FrequencyPoint
     * with the min value, the max value, the
     * mean and the standard deviation set to -1
     */
    FrequencyPoint();

    /* ! The vector input is expected to encapsulate
     *   time stamps in seconds, ordered in increasing
     *   values. This constructor computes the min,
         the max, the mean and the standard deviation
         of the corresponding frequencies.
         Note: not realtime safe.
     */
    FrequencyPoint(const std::vector<double>& timestamps);

public:
    /* ! For serialization (cereal) */
    template <class Archive>
    void serialize(Archive& archive)
    {
        archive(min, max, mean, sd);
    }

private:
    /* mean of the frequencies observed */
    double mean;
    /* minimal frequency observed */
    double min;
    /* maximal frequency observed */
    double max;
    /* standard deviation of the frequencies observed */
    double sd;
};

}  // namespace frequency_monitoring
