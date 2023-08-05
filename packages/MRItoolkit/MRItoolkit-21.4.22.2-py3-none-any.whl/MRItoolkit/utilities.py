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
import napari
from skimage.restoration import denoise_wavelet
from scipy.signal import savgol_filter



def ShowHeader(var):
    """
    ShowHeader displays method or acqp variables properly in commandline.
    Example: 
            ShowHeader(obj.method)
    """
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 999)
    print(var)


def DensityCompensation(rawdata, ksp_traj):
    """
    DensityCompensation corrects for signal energy variations in k-space.
    Example:
            rawdata = DensityCompensation(rawdata, traj):
    """
    dcf = (ksp_traj[..., 0]**2 + ksp_traj[..., 1]**2)**0.5
    rawdata = rawdata * dcf
    return rawdata


def ifft2c(x):
    """
    ifftc is a special version of inverse fast fourier transform used in phase corection.
    Example:
            ksp = ifft2c(ksp)
    """
    length = len(x.flatten())
    res = np.sqrt(length)*np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))
    return res


def fft2c(x):
    """
    ifftc is a special version of fast fourier transform used in phase corection.
    Example:
            ksp = fft2c(ksp)
    """
    length = len(x.flatten())
    res = 1/np.sqrt(length)*np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))
    return res


def PhaseCorrection(dataGrid, output):
    """
    PhaseCorrection unwraps the image phase by convolving a phase mask into the ksp.
    Example:
            ksp = PhaseCorrection(ksp, 'ksp'):
            image = PhaseCorrection(ksp, 'image'):
    """
    ham2d = np.sqrt(np.outer(np.hamming(6), np.hamming(6)))
    sx, sy = np.shape(dataGrid)
    mx, my = np.shape(ham2d)
    phase_mask = np.zeros([sx, sy])
    phase_mask[int(sx/2-mx/2): int(sx/2+mx/2),
               int(sy/2-my/2): int(sy/2+my/2)] = ham2d
    phase_mask = phase_mask/np.max(phase_mask)
    ph = ifft2c(dataGrid*phase_mask)
    ph = np.exp(1j * np.angle(ph))
    res = dataGrid * ph
    if output == "ksp":
        return res
    elif output == "image":
        res = fft2c(res)
        return res


def imshow(image, mode, rotAngle=None):
    """
    imshow is a wrap of prototype multidimension viewer called NAPARI.
    Example: 
            - 2D image: imshow(image , 'm' , rotAngle=90)
            - ND image: imshow(image , 'm' )
    """
    if mode == 'mag':
        image = np.abs(image)
    elif mode == 'phase':
        image = np.real(np.angle(image))
    elif mode == 'real':
        image = np.real(image)
    elif mode == 'imag':
        image = np.imag(image)

    if len(np.shape(image))==2:
        if rotAngle is not None:
            image = skimage.transform.rotate((image), rotAngle, resize=True)

    with napari.gui_qt():
        viewer = napari.view_image(image, rgb=False)


def signaltonoise(a, axis=0, ddof=0):
    """
    signaltonoise measure the total image SNR.
    Example:
            SNR = signaltonoise(image)
    """
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)


def CreateMask(rawdata, traj, oshape, thresh):
    """
    CreateMask retruns a nice mask of the real sampled ksp positions in cartesain space.
    Example:
            mask =  CreateMask(rawdata, traj, [256,256], 0.005)
    """
    rawdata = DensityCompensation(rawdata, traj)
    rawdata = sp.gridding(rawdata, traj, oshape)
    rawdata = np.fft.fftshift(rawdata)
    rawdata = rawdata / np.max(rawdata)
    mask = np.abs(rawdata) > thresh
    return mask


def CreateTrajectory(ttype, dtype, TrajX, TrajY, NPro, ACQ_Matrix, TrajScale, RotAngles=None):
    

    if ttype == "coRadial":
        TrajX = TrajX * ACQ_Matrix[0]
        temp = np.squeeze(npm.repmat(TrajScale[0], len(TrajX), 1))
        TrajX = TrajX * temp

        TrajY = TrajY * ACQ_Matrix[0]
        temp = np.squeeze(npm.repmat(TrajScale[1], len(TrajY), 1))
        TrajY = TrajY * temp

        if RotAngles is None:
            rot = np.linspace(0, 2*np.pi - (2*np.pi / NPro), NPro)
        else:
            rot = RotAngles

        x = []
        y = []
        for i in rot:
            si = np.cos(i)
            co = np.sin(i)
            temp_x = np.multiply(TrajX, co)
            temp_y = np.multiply(TrajY, si)
            x.append(temp_x)
            y.append(temp_y)

        if dtype == "linear":
            x_linear = []
            for row in x:
                for col in row:
                    x_linear.append(col)

            y_linear = []
            for row in y:
                for col in row:
                    y_linear.append(col)

            x_linear = [item/ACQ_Matrix[0] for item in x_linear]
            y_linear = [item/ACQ_Matrix[1] for item in y_linear]

            ksp_traj = []
            for col in y_linear:
                x_linear.append(col)
            ksp_traj = np.reshape(x_linear, (2, NPro*len(TrajX)))
            ksp_traj = np.swapaxes(ksp_traj, 0, 1)
            print("trajectory size is : " + str(np.shape(ksp_traj)))
            print('trajectory is created')
            return ksp_traj

        if dtype == "illinear":
            ksp_trajX = x
            ksp_trajY = y
            ksp_traj = np.zeros([NPro, len(TrajX), 2])
            ksp_traj[:, :, 0] = ksp_trajX
            ksp_traj[:, :, 1] = ksp_trajY
            print(np.shape(ksp_traj))
            print("trajectory size is : " + str(np.shape(ksp_traj)))
            print('trajectory is created')
            return ksp_traj


def NavigatorAnalysis(NavND,rawdataND,channels=None):
    NavND = np.mean(NavND[:, :, :, 0:5], axis=-1)
    Nav1D = NavND.flatten()
    counter = 0
    while counter<2:
        Nav1D_denoise = denoise_wavelet(np.abs(Nav1D), method='VisuShrink', mode='soft', wavelet_levels=3, wavelet='bior5.5', rescale_sigma='True')
        if counter==1:
            Nav1D_denoise = savgol_filter(Nav1D_denoise, Frames_num-Frames_var, 5)
        initial_label = np.r_[True, Nav1D_denoise[1:] > Nav1D_denoise[:-1]] & np.r_[Nav1D_denoise[:-1] > Nav1D_denoise[1:], True]

        RR = []
        c = 0
        for i in initial_label:
            # print (i)
            if i == False:
                c = c+1
            elif i == True:
                if c > 25 or c < 7:
                    c = 0
                else:
                    RR.append(c)
                    c = 0

        Frames_num = int(statistics.mode(RR))
        Frames_var = int(np.floor(statistics.stdev(RR)))
        if counter==1:
            Frames_max = int(np.max(RR))
            Frames_opt = int(Frames_num - Frames_var)

        counter=counter+1

    print('Potential number of frames:      ' + str(Frames_num))
    print('Temporal variation (in frames):  ' + str(Frames_var))
    print('Optimal number of frames:        ' + str(Frames_opt))

    if channels is None:
        rawdataND_flattend = copy.copy(rawdataND)
        rawdataND_flattend = np.reshape(rawdataND_flattend, (np.shape(RotationAngles)[0],np.shape(rawdataND_flattend)[-1]))

        

