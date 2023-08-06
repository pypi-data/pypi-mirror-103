from Classification.Parameter.LinearPerceptronParameter cimport LinearPerceptronParameter


cdef class MultiLayerPerceptronParameter(LinearPerceptronParameter):

    cdef int __hiddenNodes

    cpdef int getHiddenNodes(self)
