#include <boost/python.hpp>
#include <valarray>
#include <vector>
#include "emsfield.h"

static double DArrayGetAt(const darray &arr, size_t n) {
    if (n >= arr.size()) {
        std::__throw_out_of_range_fmt(__N("out_of_range"));
    }
    return arr[n];
}

BOOST_PYTHON_MODULE(ems) {  
    using namespace boost::python;

    class_<Field>("Field",
        init<int, int>())
        .def("SetXY", &Field::SetXY)
        .def("BulkInit", (void (Field::*)(int, double, double, int))&Field::BulkInit)
        .def("AddSpring", &Field::AddSpring)
        .def("Move", &Field::Move)
        .def("Energy", &Field::Energy)
        .def("Positions", &Field::Positions, return_internal_reference<>())
        ;

    class_<darray>("darray")
        .def("__getitem__", DArrayGetAt)
        .def("__len__", &darray::size)
        ;
}