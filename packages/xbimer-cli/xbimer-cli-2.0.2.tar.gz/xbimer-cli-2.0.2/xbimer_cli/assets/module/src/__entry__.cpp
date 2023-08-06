#include "stdafx.h"

#include "Python.h"
#include "pybind11.h"
#include "xbimer-cast.h"

// https://pybind11.readthedocs.io/en/stable/
using namespace pybind11;

#define PROJECT_VERSION "1.0.0"



PYBIND11_MODULE(__entry__, m) {
	m.add_object("version", str(PROJECT_VERSION));//Please do not delete the module version number
}