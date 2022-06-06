import numpy as np
import wfdb

def QRSComplex(vx,peaks,start=100,before=145): #record, peaks, 
    periods = []
    maxPeak = max(vx) #max amplitud of the peaks (qrs)
    diff = [maxPeak - vx[peak] for peak in peaks] #get the offset of each period
    last_peak = len(peaks)
    for i in range(last_peak): #for each QRS complex
        if i==0: sam_i=start
        else: sam_i = peaks[i]-before
        if i==last_peak-1: sam_f=len(vx)-1
        else: sam_f = peaks[i+1]-before
        periods.append(vx[sam_i:sam_f]-diff[i])
    return periods

def maxLength(QRSComplex): #Compute the width of image
    max_len = len(QRSComplex[0])
    for qrs_p in QRSComplex[1:]:
        if len(qrs_p) > max_len:
            max_len = len(qrs_p)
    return max_len

def ECG3D(QRSComplex):
    numQRS = len(QRSComplex) #number of qrs complex
    max_len = maxLength(QRSComplex)  # Compute max length of qrs complex
    ECG3D = np.zeros([numQRS, max_len]) #Matrix for ECG3D
    for i,qrs_p in enumerate(QRSComplex): #Storage each QRSComplex in a row
        index = len(qrs_p)
        ECG3D[i,:index] = qrs_p 
    return ECG3D

def makeECG3D(readPath,fileName,start=100,before=145):
    record = wfdb.rdrecord(readPath) #get record
    ecg = record.p_signal[:,1] #get only ecg signal
    annotation = wfdb.rdann(readPath,'ecg') #get annotations
    peaks = annotation.sample #get peaks
    periods = QRSComplex(ecg,peaks,start,before) #get a list of periods
    np.savetxt(fileName, ECG3D(periods), fmt='%1.7e')
    return 