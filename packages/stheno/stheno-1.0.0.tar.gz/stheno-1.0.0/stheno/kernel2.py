import logging

import alge
import numpy as np
from algebra.util import identical, to_tensor
from lab import B
from matrix import Dense, LowRank, Diagonal, Zero, Constant, AbstractMatrix
from plum import Dispatcher, Self, convert, Union

from . import PromisedFDD as FDD
from .input import Input, Unique, WeightedUnique, MultiInput
from .util import num_elements, uprank

__all__ = [
    "Kernel",
    "OneKernel",
    "ZeroKernel",
    "ScaledKernel",
    "EQ",
    "RQ",
    "Matern12",
    "Exp",
    "Matern32",
    "Matern52",
    "Delta",
    "FixedDelta",
    "Linear",
    "DerivativeKernel",
    "DecayingKernel",
    "LogKernel",
]

log = logging.getLogger(__name__)

_dispatch = Dispatcher()


class Delta(Kernel):
    """Kronecker delta kernel.

    Args:
        epsilon (float, optional): Tolerance for equality in squared distance.
            Defaults to `1e-10`.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, epsilon=1e-10):
        self.epsilon = epsilon

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        if x is y:
            return B.fill_diag(B.one(x), num_elements(x))
        else:
            return Dense(self._compute(B.pw_dists2(x, y)))

    @_dispatch(Unique, Unique)
    def __call__(self, x, y):
        x, y = x.get(), y.get()
        if x is y:
            return B.fill_diag(B.one(x), num_elements(x))
        else:
            return Zero(B.dtype(x), num_elements(x), num_elements(y))

    @_dispatch(WeightedUnique, WeightedUnique)
    def __call__(self, x, y):
        w_x, w_y = x.w, y.w
        x, y = x.get(), y.get()
        if x is y:
            return Diagonal(1 / w_x)
        else:
            return Zero(B.dtype(x), num_elements(x), num_elements(y))

    @_dispatch(Unique, object)
    def __call__(self, x, y):
        x = x.get()
        return Zero(B.dtype(x), num_elements(x), num_elements(y))

    @_dispatch(object, Unique)
    def __call__(self, x, y):
        y = y.get()
        return Zero(B.dtype(x), num_elements(x), num_elements(y))

    @_dispatch(Unique, Unique)
    def elwise(self, x, y):
        x, y = x.get(), y.get()
        if x is y:
            return B.ones(B.dtype(x), num_elements(x), 1)
        else:
            return B.zeros(B.dtype(x), num_elements(x), 1)

    @_dispatch(WeightedUnique, WeightedUnique)
    def elwise(self, x, y):
        w_x, w_y = x.w, y.w
        x, y = x.get(), y.get()
        if x is y:
            return uprank(1 / w_x)
        else:
            return B.zeros(B.dtype(x), num_elements(x), 1)

    @_dispatch(Unique, object)
    def elwise(self, x, y):
        x = x.get()
        return B.zeros(B.dtype(x), num_elements(x), 1)

    @_dispatch(object, Unique)
    def elwise(self, x, y):
        return B.zeros(B.dtype(x), num_elements(x), 1)

    @_dispatch(B.Numeric, B.Numeric)
    def elwise(self, x, y):
        if x is y:
            return B.ones(B.dtype(x), num_elements(x), 1)
        else:
            return self._compute(B.ew_dists2(x, y))

    def _compute(self, dists2):
        dtype = B.dtype(dists2)
        return B.cast(dtype, B.lt(dists2, B.cast(dtype, self.epsilon)))

    @property
    def _stationary(self):
        return True

    @_dispatch(Self)
    def __eq__(self, other):
        return self.epsilon == other.epsilon


class FixedDelta(Kernel):
    """Kronecker delta kernel that produces a diagonal matrix with given
    noises if and only if the inputs are identical and of the right shape.

    Args:
        noises (vector): Noises.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, noises):
        self.noises = noises

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        if x is y and num_elements(x) == B.shape(self.noises)[0]:
            return Diagonal(self.noises)
        else:
            return Zero(B.dtype(x), num_elements(x), num_elements(y))

    @_dispatch(B.Numeric, B.Numeric)
    def elwise(self, x, y):
        if x is y and num_elements(x) == B.shape(self.noises)[0]:
            return uprank(self.noises)
        else:
            return Zero(B.dtype(x), num_elements(x), 1)

    @property
    def _stationary(self):
        return True

    @_dispatch(Self)
    def __eq__(self, other):
        return B.all(self.noises == other.noises)

class PosteriorKernel(Kernel):
    """Posterior kernel.

    Args:
        k_ij (:class:`.kernel.Kernel`): Kernel between processes
            corresponding to the left input and the right input respectively.
        k_zi (:class:`.kernel.Kernel`): Kernel between processes
            corresponding to the data and the left input respectively.
        k_zj (:class:`.kernel.Kernel`): Kernel between processes
            corresponding to the data and the right input respectively.
        z (input): Locations of data.
        K_z (matrix): Kernel matrix of data.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, k_ij, k_zi, k_zj, z, K_z):
        self.k_ij = k_ij
        self.k_zi = k_zi
        self.k_zj = k_zj
        self.z = z
        self.K_z = convert(K_z, AbstractMatrix)

    @_dispatch(object, object)
    def __call__(self, x, y):
        return B.subtract(
            self.k_ij(x, y), B.iqf(self.K_z, self.k_zi(self.z, x), self.k_zj(self.z, y))
        )

    @_dispatch(object, object)
    def elwise(self, x, y):
        iqf_diag = B.iqf_diag(self.K_z, self.k_zi(self.z, x), self.k_zj(self.z, y))
        return B.subtract(self.k_ij.elwise(x, y), B.expand_dims(iqf_diag, axis=1))


class CorrectiveKernel(Kernel):
    """Kernel that adds the corrective variance in sparse conditioning.

    Args:
        k_zi (:class:`.kernel.Kernel`): Kernel between the processes corresponding to
            the left input and the inducing points respectively.
        k_zj (:class:`.kernel.Kernel`): Kernel between the processes corresponding to
            the right input and the inducing points respectively.
        z (input): Locations of the inducing points.
        A (tensor): Corrective matrix.
        L (tensor): Kernel matrix of the inducing points.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, k_zi, k_zj, z, A, K_z):
        self.k_zi = k_zi
        self.k_zj = k_zj
        self.z = z
        self.A = A
        self.L = B.cholesky(convert(K_z, AbstractMatrix))

    @_dispatch(object, object)
    def __call__(self, x, y):
        return B.iqf(
            self.A,
            B.solve(self.L, self.k_zi(self.z, x)),
            B.solve(self.L, self.k_zj(self.z, y)),
        )

    @_dispatch(object, object)
    def elwise(self, x, y):
        return B.iqf_diag(
            self.A,
            B.solve(self.L, self.k_zi(self.z, x)),
            B.solve(self.L, self.k_zj(self.z, y)),
        )[:, None]

