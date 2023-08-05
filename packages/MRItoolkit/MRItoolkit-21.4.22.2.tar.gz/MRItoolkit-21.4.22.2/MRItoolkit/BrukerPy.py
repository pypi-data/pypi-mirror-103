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

class Bruker_tools:
    """
    Bruker_tools is a python class containing the following functionalities  
        - _ReadBrukerParameterFile: reads Bruker parametr files, such as ACQP and METHOD
        - _GetParameter: gets a single parametrs valaue from parameter files
        - _readFIDprep: reads & truncates Bruker FID binary files
        - _readFID: masp/sorts Bruker FID file from outmost PPG loops to inmost ones 

    Args:
        -readpath: Bruker rawdata folder path
    """
    
    def __init__(self, readpath):
        self.readpath = readpath
        self.acqp = self._ReadBrukerParameterFile('acqp', self.readpath)
        self.method = self._ReadBrukerParameterFile('method', self.readpath)

        self.ACQ_size, _ = self._GetParameter("ACQ_size", 'acqp')
        self.ACQ_size = np.array(self.ACQ_size, dtype=int)

        self.nReceiver_value, _ = self._GetParameter("PVM_EncNReceivers", 'method')
        self.nReceiver_value = np.array(self.nReceiver_value, dtype=int)

    def _ReadBrukerParameterFile(self, filetype, readpath):
        """
        _ReadBrukerParameterFile reads Bruker ACQP and METHOD parameter files
        """
        readpath = readpath+"/"+filetype
        print('reading ' + filetype + ' file ' + 'from ' + readpath)

        acqp = open(readpath, mode='r')
        acqp = acqp.read().splitlines()

        ind = []
        param = []
        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0:3] == '##$':
                param.append(Row.split('=')[0][3:])
                ind.append(i)

        value = []
        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0:3] == '##$':
                value.append(Row.split('=')[1])

        size = []
        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0:3] == '##$':
                size.append('1')
        # ----------------------------------------------------

        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0:2] == '$$':
                param.append(Row.split('=')[0][3:])
                ind.append(i)

        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0:2] == '$$':
                value.append(Row.split('=')[1])

        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0:2] == '$$':
                size.append('1')

        # ----------------------------------------------------

        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0] == '<':
                param.append(Row.split('=')[0][3:])

        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0] == '<':
                value.append(nextRow)

        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and nextRow[0] == '<':
                size.append(Row.split('=')[1])

        # ----------------------------------------------------

        for i in range(0, len(acqp)-1):
            Row = acqp[i]
            nextRow = acqp[i+1]
            if Row[0:3] == '##$' and (nextRow[0].isdigit() or nextRow[0].isalpha() or nextRow[0] == '-' or nextRow[0] == '('):
                param.append(Row.split('=')[0][3:])
                size.append(Row.split('=')[1])
                counter = 1
                temp = []
                a = []
                while acqp[i+counter] != '##$':
                    a = acqp[i+counter]
                    if a[0:3] == '##$' or a[0:2] == '$$':
                        break
                    temp.append(a)
                    counter = counter+1
                    line = i+counter
                    if line == len(acqp)-1:
                        break
                value.append(temp)


        Value = pd.Series(value, param, name='value')
        Size = pd.Series(size, param, name='size')
        Value = pd.DataFrame(Value)
        Size = pd.DataFrame(Size)
        Header = Value.join(Size)

 
        print('the number of generated parameters is ' + str(len(Header)))

        paramType = []
        for ind in Header.index:
            value = Header.loc[ind, 'value']
            temp = value[0][0]
            if temp == "<" or temp == "_" or temp == "(":
                paramType.append('string')

            elif temp.isalpha():
                paramType.append('string')

            elif temp == "-":
                paramType.append('array')

            else:
                paramType.append('array')

        paramType = pd.Series(paramType, Header.index, name='paramType')
        paramType = pd.DataFrame(paramType)
        Header = Header.join(paramType)

        exclusion_list = ['PVM_TrajGeoObj', 'PVM_FovSatGeoObj', 'PVM_SliceGeoObj', 'PVM_SliceGeo', 'PVM_FovSatPul', 'PVM_MagTransPulse1', 'PVM_MagTransPulse1Ampl', 'PVM_TrajExcPulse', 'PVM_TrajRfcPulse', 'PVM_FovSatGeoCub', 'PVM_FatSupPul', 'PVM_ExportHandler', 'PVM_TrajGeoCub', 'PVM_TrajGeoCub', 'PVM_FovSatGeoCub', 'PVM_TaggingPul', 'PVM_FovSatGeoObj', 'ExcPulse1', 'PVM_FatSupPul', 'PVM_MagTransPulse1', 'PVM_FovSatPul', 'PVM_FlowSatPul']
        for i in exclusion_list:
            try:
                Header = Header.drop([i])
            except:
                pass

        savepath = readpath + '.html'
        Header.to_html(savepath)
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        return Header



    def _GetParameter(self, ParamName, Header):
        """
        Description: _GetParameter calls a specified parameters "ParamName" from the parameter file "Header". 
        Example:
            nVelocity_value, nVelocity_size = ins._GetParameter("FlowEncLoop", 'method')
        """
        if Header == "acqp":
            Header = self.acqp
        elif Header == "method":
            Header = self.method

        if Header.loc[ParamName, 'paramType'] == 'string':
            print('Fialed: ParamName data type is not defined as "ARRAY"')
        else:
            size = Header.loc[ParamName, 'size']
            size = size.replace('(', '')
            size = size.replace(')', '')
            size = size.split(',')
            size_arr = []
            for i in range(0, len(size)):
                size_arr.insert(i, int(size[i]))
            size = size_arr

            if size == [1]:
                if type(Header.loc[ParamName, 'value']) == str:
                        value = float(Header.loc[ParamName, 'value'])
                        print('parameters is generated successfully 1')
                        return value, size
                else:
                    value = float(Header.loc[ParamName, 'value'][0])
                    print('parameters is generated successfully 2')
                    return value, size
            else:
                value = []
                counter = 0
                for row in Header.loc[ParamName, 'value']:
                    temp = []
                    temp = row
                    temp = temp.split(' ')
                    temp = [el for el in temp if el != '']
                    temp_arr = []
                    for i in range(0, len(temp)):
                        value.insert(counter, float(temp[i]))
                        counter = counter+1
                value = np.reshape(value, size)
                print('parameters is generated successfully 3')
                return value, size

    def _readFIDprep(self, binaryFiletype, args):
        """
        Description: reads & trucates the FID binary file based on the readout resolution. 
        The reason for this style of rawdata programming is that, this approach immunes the 
        presence of different dimensionalities in different pulse programms 
        """
        self.binaryFiletype = binaryFiletype
        readpath = self.readpath + '/' + self.binaryFiletype

        GO_bits = np.array(32)
        GO_block_size = 'Standard_KBlock_Format'

        # This group of parametrs are necessary to read outputs of other versions of Paravision
        # GO_raw_data_format = 'GO_32BIT_SGN_INT'
        # GO_format = 'int32'
        # BYTORDA = 'little'
        # endian = 'l'
        # AQ_mod = 'qdig'
        # isComplexRaw = True
        # GO_data_save = 'Yes'
        # jobsExist = False
        # precision = 'double'

        numDataHighDim = int(np.prod(args[:-2]))
        print(numDataHighDim)
        if self.binaryFiletype == 'fid' and GO_block_size == 'Standard_KBlock_Format' :
            blockSize = mt.ceil(args[-1]*args[-2] * (GO_bits/8)/1024)*1024/(GO_bits/8)
        elif self.binaryFiletype == 'rawdata.job0' and GO_block_size == 'Standard_KBlock_Format':
            blockSize = args[-1]*args[-2]
        elif self.binaryFiletype == 'rawdata.job1':
            blockSize = args[-1]*args[-2]*2

        fid = open(readpath, mode='r')
        fid = np.fromfile(fid, dtype=np.int32)
        fid = fid.reshape(numDataHighDim, int(blockSize))
        fid = fid[:, 0:args[-1]*args[-2]]
        fid = fid.reshape(numDataHighDim, args[-2], args[-1])
        temp = fid[:, :, ::2]
        temp1 = fid[:, :, 1::2]
        rawdata = np.vectorize(complex)(temp, temp1)
        print('rawdata binary file is read successfully')
        return rawdata

    def _readFID(self, binaryFiletype, arg):
        """
        Description: _readFID reads and sorts Bruker FID binary files from outmost PPG loops to inmost ones 
        args [List]: Specify all the pulse programm loops from the outmost to the inmost as input arguments.

        Example:
            ppg = [ACQ_size[2], ACQ_size[1], nVelocity_value, nFrames_value, nReceiver_value , ACQ_size[0]]
            rawdata = obj._readFID(ppg)
        """

        data = self._readFIDprep(binaryFiletype, arg)
        arg[-1] = np.shape(data)[-1]
        rawdata = data.reshape(arg)
        rawdata = np.squeeze(rawdata)
        print('rawdata dimension chaged successfully')
        return rawdata
