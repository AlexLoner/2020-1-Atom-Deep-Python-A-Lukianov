#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "structmember.h" // alolled create attribute (PyMemberDef)

typedef struct MatrixObject {
    PyObject_HEAD
    PyObject *mtx_list;
    long rows, cols;
    PyObject *shape;
} MatrixObject;

// -------------------- __init__ method --------------------------------------
static int Matrix_init(MatrixObject *self, PyObject *args){

    PyObject *mtx_list = NULL;

    // check that inner array is a list
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &mtx_list)) {
        PyErr_SetString(PyExc_TypeError, "It's not a list.");
        return -1;
    }

    // check that rows also are list too
    self->rows = PyList_Size(mtx_list);
    long new_cols;
    for (int i = 0; i < self->rows; ++i){
        PyObject *inner = PyList_GetItem(mtx_list, i);
        if (!PyList_Check(inner)){
            PyErr_SetString(PyExc_TypeError, "Row not a list.");
            return -1;
        }
        else {
            self->cols = PyList_Size(inner);
            // check that matrix contains only by float or integers
            if ((i > 0) && (self->cols != new_cols) ) {
                PyErr_SetString(PyExc_TypeError, "Shape should be equal ");
                return -1;
            }
            for (int j = 0; j < self->cols; ++j){
                PyObject *item = PyList_GetItem(inner, j);

                if (!PyFloat_Check(item) && !PyLong_Check(item)){
                    PyErr_SetString(PyExc_TypeError, "Matrix should contains float (integer) number");
                    return -1;
                }
                // convert all valid items to float
                PyList_SetItem(inner, j, PyNumber_Float(item));
            }
            new_cols = self->cols;
        }
        }
    Py_INCREF(mtx_list);
    self->mtx_list = mtx_list; //Py_BuildValue("[iii]", 1, 2, 3);

    self->shape = PyTuple_New(2);
    PyTuple_SetItem(self->shape, 0, PyLong_FromLong(self->rows));
    PyTuple_SetItem(self->shape, 1, PyLong_FromLong(self->cols));

    return 0;
}


// -------------------- __str__ method --------------------------------------
static PyObject *Matrix_str(MatrixObject *self){
    PyObject *full = PyUnicode_FromFormat("[");
    for (int i = 0; i < self->rows; ++i){
        PyObject *ns = PyUnicode_FromFormat("[");
        PyObject *inner = PyList_GetItem(self->mtx_list, i);
        for (int j = 0; j < self->cols; ++j) {
            PyObject *num = PyList_GetItem(inner, j);
            ns = PyUnicode_Concat(ns, PyObject_Repr(num));
            if (j < self->cols - 1)
                ns = PyUnicode_Concat(ns, PyUnicode_FromFormat(" "));
        }
        full = PyUnicode_Concat(full, ns);
        full = PyUnicode_Concat(full, PyUnicode_FromFormat("]"));
        if (i < self->rows - 1)
            full = PyUnicode_Concat(full, PyUnicode_FromFormat("\n"));
    }
    full = PyUnicode_Concat(full, PyUnicode_FromFormat("]\n"));
    return full;
}


// -------------------- __repr__ method --------------------------------------
static PyObject *Matrix_repr(MatrixObject *self){
    PyObject *full = PyUnicode_FromFormat("Matrix:\n");
    full = PyUnicode_Concat(full, PyUnicode_FromFormat("["));
    for (int i = 0; i < self->rows; ++i){
        PyObject *ns = PyUnicode_FromFormat("[");
        PyObject *inner = PyList_GetItem(self->mtx_list, i);
        for (int j = 0; j < self->cols; ++j) {
            PyObject *num = PyList_GetItem(inner, j);
            ns = PyUnicode_Concat(ns, PyObject_Repr(num));
            if (j < self->cols - 1)
                ns = PyUnicode_Concat(ns, PyUnicode_FromFormat(" "));
        }
        full = PyUnicode_Concat(full, ns);
        full = PyUnicode_Concat(full, PyUnicode_FromFormat("]"));
        if (i < self->rows - 1)
            full = PyUnicode_Concat(full, PyUnicode_FromFormat("\n"));
    }
    full = PyUnicode_Concat(full, PyUnicode_FromFormat("]\n"));
    full = PyUnicode_Concat(full, PyUnicode_FromFormat("Shape: [%dx%d]\n", self->rows, self->cols));
    return full;
}


// -------------------- __getitem__ method --------------------------------------
static PyObject *Matrix_subscript(MatrixObject *self, PyObject *index){

    if (!PyTuple_Check(index)) {
        PyErr_SetString(PyExc_IndexError, "Index should be tuple with integers");
        return NULL;
    }
    if (PyTuple_Size(index) != 2){
        PyErr_SetString(PyExc_TypeError, "Incorrect index tuple should has length 2");
        return NULL;
    }
    for (int k = 0; k < 2; ++k){
        PyObject *item = PyTuple_GetItem(index, k);
        if (!PyLong_Check(item))
            PyErr_SetString(PyExc_IndexError, "Single index should be integer");
        if (item < PyLong_FromLong(0))
            PyErr_SetString(PyExc_IndexError, "Negative indexes not allowed");
    }

    PyObject *i = PyTuple_GetItem(index, 0);
    PyObject *j = PyTuple_GetItem(index, 1);
//    if ((i > PyLong_FromLong(self->rows - 1)) && (j > PyLong_FromLong(self->cols - 1))){
//        PyErr_SetString(PyExc_IndexError, "index out of range :(");
//        return NULL;
//    }
    PyObject *inner = PyObject_GetItem(self->mtx_list, i);
    PyObject *value = PyObject_GetItem(inner, j);
    return value;
}


// -------------------- setting attributes -----------------------------------
static PyMemberDef Matrix_members[] = {
    {"dense", T_OBJECT, offsetof(MatrixObject, mtx_list), 0, "Storage for matrix"},
    {"shape", T_OBJECT, offsetof(MatrixObject, shape), 0, "Matrix shape"},
    {NULL}  /* Sentinel */
};


// -------------------- setting methods ---------------------------------------
static PyMappingMethods Matrix_as_mapping = {
    .mp_subscript = (binaryfunc) Matrix_subscript,		/* mp_subscript */
};


static PyTypeObject MatrixType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "matrix.Matrix",
    .tp_doc = "Matrix object",
    .tp_basicsize = sizeof(MatrixObject),
    .tp_itemsize = 0,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc) Matrix_init,
    .tp_str = (reprfunc) Matrix_str,
    .tp_repr = (reprfunc) Matrix_repr,
    .tp_members = Matrix_members,
    .tp_as_mapping = &Matrix_as_mapping,
};



static PyModuleDef matrixmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "matrix",
    .m_doc = "My matrix module",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_matrix(void) {
    PyObject *m;
    if (PyType_Ready(&MatrixType) < 0)
        return NULL;

    m = PyModule_Create(&matrixmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&MatrixType);
    if (PyModule_AddObject(m, "Matrix", (PyObject *) &MatrixType) < 0) {
        Py_DECREF(&MatrixType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}