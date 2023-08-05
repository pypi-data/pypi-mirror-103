import matplotlib.pyplot as plt
import matplotlib.image as Image
import scipy.io as sio
import pandas as pd
import numpy as np
import numpy.matlib as npm
import math as mt
import cmath
from itertools import permutations
import mpld3
from pynufft import NUFFT
from pynufft.linalg import solve_cpu
import skimage.transform
import skimage
import sigpy as sp
import sigpy.mri as mr
import sigpy.plot as pl
import BrukerPy
import utilities
import numpy.matlib


def FiniteDifference_2ndOrd(ishape, axes=None):

    I = sp.linop.Identity(ishape)
    ndim = len(ishape)
    axes = sp.util._normalize_axes(axes, ndim)
    linops = []
    for i in axes:
        D = I - sp.linop.Circshift(ishape, [1], axes=[i])
        D = D*D
        R = sp.linop.Reshape([1] + list(ishape), ishape)
        linops.append(R * D)

    G = sp.linop.Vstack(linops, axis=0)

    return G




class TV_Reco_L2_G1pG2(sp.app.LinearLeastSquares):

    def __init__(self, image, mask, lamda, max_iter, show_pbar=False):

        img_shape = image.shape
        P = sp.linop.Multiply(img_shape, mask)
        F = sp.linop.FFT(img_shape)
        self.dataGrid = F * (image) #/ np.mean(image))
        # self.dataGrid = self.dataGrid / np.max(self.dataGrid)
        A = P * F

        G2 = FiniteDifference_2ndOrd(A.ishape)
        G1 = sp.linop.FiniteDifference(A.ishape)
        G = []
        G.append(G1)
        G.append(G2)
        G = sp.linop.Vstack(G, axis=0)
        proxg = sp.prox.L1Reg(G.oshape, lamda)

        def g(x):
            return np.sum(np.abs(x)).item()

        super().__init__(A, self.dataGrid, proxg=proxg, g=g,
                         G=G, max_iter=max_iter, show_pbar=show_pbar)




class CS_Reco(sp.app.App):
    def __init__(self, image, mask, lamda, max_iter):

        img_shape = image.shape
        alpha = 1

        F = sp.linop.FFT(img_shape)
        self.dataGrid = F*image
        self.dataGrid = self.dataGrid

        P = sp.linop.Multiply(self.dataGrid.shape, mask)
        self.W = sp.linop.Wavelet(img_shape, wave_name='db4', level=1)

        A = P * F * self.W.H

        proxg = sp.prox.L1Reg(A.ishape, lamda)

        self.wav = np.zeros(A.ishape, np.complex)

        def gradf(x):
            return A.H * (A * x - self.dataGrid)

        alg = sp.alg.GradientMethod(
            gradf, self.wav, alpha, proxg=proxg, max_iter=max_iter)
        super().__init__(alg, show_pbar=False, leave_pbar=False)

    def _output(self):
        return self.W.H(self.wav)




class TV_Reco(sp.app.LinearLeastSquares):

    def __init__(self, image, mask, lamda, max_iter, show_pbar=False):

        img_shape = image.shape
        P = sp.linop.Multiply(img_shape, mask)
        F = sp.linop.FFT(img_shape)
        self.dataGrid = F * image
        # self.dataGrid = self.dataGrid / np.max(self.dataGrid)
        A = P * F

        G = sp.linop.FiniteDifference(A.ishape)
        proxg = sp.prox.L1Reg(G.oshape, lamda)

        def g(x):
            return lamda * np.sum(np.abs(x)).item()

        super().__init__(A, self.dataGrid, proxg=proxg, g=g,
                         G=G, max_iter=max_iter, show_pbar=show_pbar)




class TV_CS_Reco(sp.app.LinearLeastSquares):

    def __init__(self, image, mask, lamda, max_iter, RecoType, **kwargs):

        img_shape = np.shape(image)
        self.RecoType = RecoType

        F = sp.linop.FFT(img_shape)
        P = sp.linop.Multiply(img_shape, mask)
        self.ksp = F * image
        self.ksp = self.ksp / np.max(self.ksp)

        self.W = sp.linop.Wavelet(img_shape)
        if self.RecoType == "CSTV":
            wav = self.W * P * F.H * self.ksp
            A = P * F * self.W.H
        elif self.RecoType == "TV":
            wav = P * F.H * self.ksp
            A = P * F

        G = sp.linop.FiniteDifference(A.ishape)
        proxg = sp.prox.L1Reg(G.oshape, lamda)
        self.wav = np.zeros(A.ishape, np.complex)

        def g(x):
            with device:
                return lamda * np.sum(np.abs(np.fft.fftshift(x))).item()
        super().__init__(A, self.ksp, self.wav, proxg=proxg, g=g, G=G,
                         max_iter=max_iter, show_pbar=False, leave_pbar=False, **kwargs)

    def _output(self):
        if self.RecoType == "CSTV":
            return self.W.H(self.wav)
        elif self.RecoType == "TV":
            return self.wav

    def getSolver(self):
        return self.solver


def estimate_weights(y, weights, coord):
    if weights is None and coord is None:
        weights = (sp.rss(y, axes=(0, )) > 0).astype(y.dtype)

    return weights


class L1WaveletRecon(sp.app.App):
    def __init__(self, ksp, mask, traj, img_shape, lamda, max_iter):
        F = sp.linop.IFFT(img_shape)
        P = sp.linop.Multiply(ksp.shape, mask)
        self.W = sp.linop.Wavelet(img_shape)
        A = F * self.W.H

        proxg = sp.prox.L1Reg(A.ishape, lamda)

        self.wav = np.zeros(A.ishape, np.complex)
        alpha = 1

        def gradf(x):
            return A.H * (A * x - ksp)

        alg = sp.alg.GradientMethod(gradf, self.wav, alpha, proxg=proxg,
                                    max_iter=max_iter)
        super().__init__(alg)

    def _output(self):
        return self.W.H(self.wav)
