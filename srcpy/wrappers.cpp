#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "frequency_monitoring/frequency_point.hpp"
#include "shared_memory/shared_memory.hpp"

using namespace frequency_monitoring;

PYBIND11_MODULE(frequency_monitoring_wrp, m)
{
    pybind11::class_<FrequencyPoint>(m, "FrequencyPoint")
        .def(pybind11::init<>())
        .def("set", &FrequencyPoint::set)
        .def_readwrite("mean", &FrequencyPoint::mean)
        .def_readonly("sd", &FrequencyPoint::sd)
        .def_readonly("min", &FrequencyPoint::min)
        .def_readonly("max", &FrequencyPoint::max);

    m.def("serialize",
          [](const std::string& segment_id, const FrequencyPoint& fp) {
              shared_memory::serialize<FrequencyPoint>(
                  segment_id, segment_id, fp);
          });

    m.def("deserialize", [](const std::string& segment_id, FrequencyPoint& fp) {
        shared_memory::deserialize<FrequencyPoint>(segment_id, segment_id, fp);
    });
}
