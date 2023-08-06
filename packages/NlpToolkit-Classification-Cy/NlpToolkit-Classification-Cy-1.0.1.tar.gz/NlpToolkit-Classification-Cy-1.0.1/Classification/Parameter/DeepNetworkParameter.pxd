from Classification.Parameter.LinearPerceptronParameter cimport LinearPerceptronParameter


cdef class DeepNetworkParameter(LinearPerceptronParameter):

    cdef list __hiddenLayers

    cpdef int layerSize(self)
    cpdef int getHiddenNodes(self, int layerIndex)
