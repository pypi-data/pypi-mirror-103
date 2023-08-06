#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "kPointLatticeGenerator.h"
#include "kPointLattice.h"


namespace py = pybind11;

PYBIND11_MODULE(lib, m) {

    m.doc() = "kpLib C++ interface";


 	py::enum_<INCLUDE_GAMMA> include_gamma(m,"INCLUDE_GAMMA");
 	include_gamma.value("TRUE",INCLUDE_GAMMA::TRUE);
	include_gamma.value("FALSE",INCLUDE_GAMMA::FALSE);
	include_gamma.value("AUTO",INCLUDE_GAMMA::AUTO);


	py::class_<KPointLattice> kpLattice(m,"KPointLattice");
	kpLattice.def("getSuperToDirect",&KPointLattice::getSuperToDirect);
	kpLattice.def("getShift",&KPointLattice::getShift);
	kpLattice.def("getMinPeriodicDistance",&KPointLattice::getMinPeriodicDistance);
	kpLattice.def("getNumDistinctKPoints",&KPointLattice::getNumDistinctKPoints);
	kpLattice.def("getSuperToDirect",&KPointLattice::getSuperToDirect);
	kpLattice.def("numTotalKPoints", &KPointLattice::numTotalKPoints);
	kpLattice.def("getKPointCoordinates", &KPointLattice::getKPointCoordinates);
	kpLattice.def("getKPointWeights", &KPointLattice::getKPointWeights);


 	py::class_<KPointLatticeGenerator> kpLib(m, "KPointLatticeGenerator");
 	kpLib.def(py::init<Tensor<double>,Tensor<double>,std::vector<Tensor<int>>,const bool>());
	kpLib.def("getKPointLattice", (KPointLattice (KPointLatticeGenerator::*)(const double, const int))  &KPointLatticeGenerator::getKPointLattice);
 	kpLib.def("includeGamma",&KPointLatticeGenerator::includeGamma);
 	kpLib.def("useScaleFactor", &KPointLatticeGenerator::useScaleFactor);

}
