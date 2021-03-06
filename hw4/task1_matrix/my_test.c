#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include "structmember.h" // alolled create attribute (PyMemberDef)

static PyTypeObject MatrixType;

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


// -------------------- __repr__ method --------------------------------------
static PyObject *Matrix_repr(MatrixObject *self){
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


// -------------------- __add__ method --------------------------------------
static MatrixObject *Matrix_add(MatrixObject *self, MatrixObject *other){
    if ((self->rows != other->rows) || (self->cols != other->cols)) {
        PyErr_SetString(PyExc_ValueError, "dimension should be equal");
        return NULL;
        }

    // Create new instance
    MatrixObject *obj;
    obj = PyObject_New(MatrixObject, &MatrixType);
    PyObject_Init((PyObject *)obj, &MatrixType);
    obj->mtx_list = PyList_New(self->rows);
    obj->rows = self->rows;
    obj->cols = self->cols;
    obj->shape = self->shape;

    PyObject *s1, *s2;
    for (int i = 0; i < self->rows; ++i) {
        PyList_SetItem(obj->mtx_list, i, PyList_New(self->cols));
        for (int j = 0; j < self->cols; ++j){
            s1 = PyList_GetItem(PyList_GetItem(self->mtx_list, i), j);
            s2 = PyList_GetItem(PyList_GetItem(other->mtx_list, i), j);
            PyList_SetItem(PyList_GetItem(obj->mtx_list, i), j, PyNumber_Add(s1, s2));
        }
    }
    return obj;
}


// -------------------- __sub__ method --------------------------------------
static MatrixObject *Matrix_substract(MatrixObject *self, MatrixObject *other){
    if ((self->rows != other->rows) || (self->cols != other->cols)) {
        PyErr_SetString(PyExc_ValueError, "dimension should be equal");
        return NULL;
        }

    // Create new instance
    MatrixObject *obj;
    obj = PyObject_New(MatrixObject, &MatrixType);
    PyObject_Init((PyObject *)obj, &MatrixType);
    obj->mtx_list = PyList_New(self->rows);
    obj->rows = self->rows;
    obj->cols = self->cols;
    obj->shape = self->shape;

    PyObject *s1, *s2;
    for (int i = 0; i < self->rows; ++i) {
        PyList_SetItem(obj->mtx_list, i, PyList_New(self->cols));
        for (int j = 0; j < self->cols; ++j){
            s1 = PyList_GetItem(PyList_GetItem(self->mtx_list, i), j);
            s2 = PyList_GetItem(PyList_GetItem(other->mtx_list, i), j);
            PyList_SetItem(PyList_GetItem(obj->mtx_list, i), j, PyNumber_Subtract(s1, s2));
        }
    }
    return obj;
}


// -------------------- __mul__ method --------------------------------------
static MatrixObject *Matrix_mul(MatrixObject *self, PyObject *number){

    // Create new instance
    MatrixObject *obj;
    obj = PyObject_New(MatrixObject, &MatrixType);
    PyObject_Init((PyObject *)obj, &MatrixType);
    obj->mtx_list = PyList_New(self->rows);
    obj->rows = self->rows;
    obj->cols = self->cols;
    obj->shape = self->shape;

    PyObject *s1;
    for (int i = 0; i < self->rows; ++i) {
        PyList_SetItem(obj->mtx_list, i, PyList_New(self->cols));
        for (int j = 0; j < self->cols; ++j){
            s1 = PyList_GetItem(PyList_GetItem(self->mtx_list, i), j);
            PyList_SetItem(PyList_GetItem(obj->mtx_list, i), j, PyNumber_Multiply(s1, PyNumber_Float(number)));
        }
    }
    return obj;
}

static MatrixObject *Matrix_multiply(PyObject *var1, PyObject *var2){
    if (PyObject_IsInstance(var1, (PyObject *)&MatrixType) && PyNumber_Check(var2)){
        return Matrix_mul((MatrixObject *) var1, var2);
    }
    else if (PyObject_IsInstance(var2, (PyObject *)&MatrixType) && PyNumber_Check(var1)) {
        return Matrix_mul((MatrixObject *) var2, var1);
    }
    else {
        PyErr_SetString(PyExc_ValueError, "Non-valid input");
        return NULL;
    }
}

// -------------------- __truediv__ method --------------------------------------
static MatrixObject *Matrix_div(MatrixObject *self, PyObject *number){
    if (PyNumber_Float(number) == PyFloat_FromDouble(0.0)) {
        PyErr_SetString(PyExc_ZeroDivisionError, "Division by zero, not cool man");
        return NULL;
        }

    // Create new instance
    MatrixObject *obj;
    obj = PyObject_New(MatrixObject, &MatrixType);
    PyObject_Init((PyObject *)obj, &MatrixType);
    obj->mtx_list = PyList_New(self->rows);
    obj->rows = self->rows;
    obj->cols = self->cols;
    obj->shape = self->shape;

    PyObject *s1;
    for (int i = 0; i < self->rows; ++i) {
        PyList_SetItem(obj->mtx_list, i, PyList_New(self->cols));
        for (int j = 0; j < self->cols; ++j){
            s1 = PyList_GetItem(PyList_GetItem(self->mtx_list, i), j);
            PyList_SetItem(PyList_GetItem(obj->mtx_list, i), j, PyNumber_TrueDivide(s1, PyNumber_Float(number)));
        }
    }
    return obj;
}

static MatrixObject *Matrix_TrueDivide(PyObject *var1, PyObject *var2){
    if (PyObject_IsInstance(var1, (PyObject *)&MatrixType) && PyNumber_Check(var2)){
        return Matrix_div((MatrixObject *) var1, var2);
    }
    else {
        PyErr_SetString(PyExc_ValueError, "Non-valid input");
        return NULL;
    }
}

// -------------------- __matmul__ method ---------------------------------------
static MatrixObject *Matrix_matmul(MatrixObject *self, MatrixObject *other){

    if (!PyObject_IsInstance(self, (PyObject *) &MatrixType) || !PyObject_IsInstance(other, (PyObject *) &MatrixType)){
        PyErr_SetString(PyExc_ValueError, "Not Matrix object(s)");
        return NULL;
    }

    if (self->cols != other->rows){
        PyErr_SetString(PyExc_ValueError, "Wrong dimensions");
        return NULL;
    }

    MatrixObject *obj;
    obj = PyObject_New(MatrixObject, &MatrixType);
    PyObject_Init((PyObject *)obj, &MatrixType);
    obj->mtx_list = PyList_New(self->rows);
    obj->rows = self->rows;
    obj->cols = other->cols;
    obj->shape = PyTuple_New(2);
    PyTuple_SetItem(obj->shape, 0, PyLong_FromLong(obj->rows));
    PyTuple_SetItem(obj->shape, 1, PyLong_FromLong(obj->cols));

    PyObject *n1, *n2, *tmp, *temp;
    for (int i = 0; i < self->rows; ++i) {
        PyList_SetItem(obj->mtx_list, i, PyList_New(obj->cols));
        for (int j = 0; j < other->cols; ++j) {
            temp = PyFloat_FromDouble(0.0);
            for (int k = 0; k < other->rows; ++k) {
                n1 = PyList_GetItem(PyList_GetItem(self->mtx_list, i), k);
                n2 = PyList_GetItem(PyList_GetItem(other->mtx_list, k), j);
                temp = PyNumber_Add(temp, PyNumber_Multiply(n1, n2));
            }
            PyList_SetItem(PyList_GetItem(obj->mtx_list, i), j, temp);
        }
    }
    return obj;
}

// -------------------- transpose method ----------------------------------------
static MatrixObject * Matrix_transpose(MatrixObject *self)
{
    // Create new instance
    MatrixObject *obj;
    obj = PyObject_New(MatrixObject, &MatrixType);
    PyObject_Init((PyObject *)obj, &MatrixType);
    obj->mtx_list = PyList_New(self->cols);
    obj->rows = self->cols;
    obj->cols = self->rows;
    obj->shape = PyTuple_New(2);
    PyTuple_SetItem(obj->shape, 0, PyLong_FromLong(obj->rows));
    PyTuple_SetItem(obj->shape, 1, PyLong_FromLong(obj->cols));


    PyObject *number;
    for (int i = 0; i < obj->rows; ++i) {
        PyList_SetItem(obj->mtx_list, i, PyList_New(obj->cols));
        for (int j = 0; j < obj->cols; ++j){
            number = PyList_GetItem(PyList_GetItem(self->mtx_list, j), i);
            PyList_SetItem(PyList_GetItem(obj->mtx_list, i), j, PyNumber_Float(number));
        }
    }
    return obj;
}


// -------------------- setting attributes -----------------------------------
static PyMemberDef Matrix_members[] = {
    {"dense", T_OBJECT, offsetof(MatrixObject, mtx_list), 0, "Storage for matrix"},
    {"shape", T_OBJECT, offsetof(MatrixObject, shape), 0, "Matrix shape"},
    {NULL}  /* Sentinel */
};

// -------------------- setting methods ---------------------------------------
static PyMethodDef Matrix_methods[] = {
//    { "sum", sample_sum, METH_VARARGS, "sum of elements of the list" },
    {"transpose", Matrix_transpose, METH_VARARGS, "Transpose matrix"},
    { NULL, NULL, 0, NULL }
};


// -------------------- PyTypeObjects features --------------------------------
static PyNumberMethods Matrix_as_number = {
     .nb_add = (binaryfunc) Matrix_add,
     .nb_subtract = (binaryfunc) Matrix_substract,
     .nb_multiply = (binaryfunc) Matrix_multiply,
     .nb_true_divide = (binaryfunc) Matrix_TrueDivide,
     .nb_matrix_multiply = (binaryfunc) Matrix_matmul,
};


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
    .tp_methods = Matrix_methods,
    .tp_as_mapping = &Matrix_as_mapping,
    .tp_as_number = &Matrix_as_number,
};

// -------------------- module creation procedures -------------------------
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
