#include <boost/python.hpp>
#include "common.h"

Timer g_Timer(true);

BOOST_PYTHON_MODULE(perftest) {  
    boost::python::def("testVector", noavx::TestVector);
    boost::python::def("testValArray", noavx::TestValArray);
    boost::python::def("testEigen", noavx::TestEigen);
    boost::python::def("testVectorV", avx::TestVector);
    boost::python::def("testValArrayV", avx::TestValArray);
    boost::python::def("testEigenV", avx::TestEigen);
}