#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:30:24 2018

@author: chriscrossing
"""
import re
import numpy as np
import pickle

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def OSAStat(OSA): #Checks what state the OSA is in.
    OSA.write("SWEEP?");
    print("Value: " + str(re.sub("\D", "", OSA.read(10).decode('UTF-8'))))
    return 

def Init(TLS,OSA):
    OSA.write("INIT");
    TLS.write("INIT");
    return

def stop(OSA):
    OSA.write("STP")
    return

def savedefault(TLS_default,OSA_default,Common_default,Power,
        Swp_Step,Swp_Time,Stp_Time,Ave_rpts,
        Resolution,Samples,Swp_Start,Swp_End):
    
    newTLS = {
            'Power': Power,
            'Swp_Step': Swp_Step,
            'Swp_Time': Swp_Time,
            'Stp_Time': Stp_Time
            }
    newOSA = {
            'Ave_rpts': Ave_rpts,
            'Resolution': Resolution,
            'Samples': Samples
            }
    newcommon = {
            'Swp_Start': Swp_Start,
            'Swp_End': Swp_End
            }
    
    TLS_default.update(newTLS)
    OSA_default.update(newOSA)
    Common_default.update(newcommon)
    save_obj(TLS_default, 'TLS_default')
    save_obj(OSA_default, 'OSA_default')
    save_obj(Common_default, 'Common_default')
    return

def single(TLS,OSA,Wavelength,Power):
    TLS.write("TWL" + str(Wavelength))
    TLS.write("TPMW" + str(Power)) 
    TLS.write("L1") # Turns on laser
    OSA.write("AUTO") # Auto scanning
    input("Press Enter when finished")
    OSA.write("STP") #stops sweeping
    TLS.write("L0") #laser off
    return

def swp_init(TLS,OSA,TLS_default,Power,Swp_Start,Swp_End,Samples,Ave_rpts,Swp_Step,Swp_Time,Stp_Time,Resolution,Sensitivity):

    TLS.write("TPMW" + str(Power)); 
    TLS.write("TSTPWL" + str(Swp_End));
    TLS.write("TSTAWL" + str(Swp_Start));
    TLS.write("TSTEWL" + str(Swp_Step));
    TLS.write("TSWET" + str(Swp_Time));
    TLS.write("TSTET" + str(Stp_Time));
    OSA.write("RESOLN" + str(Resolution));
    OSA.write("TLSADR" + str(TLS_default.get('adr')));
    OSA.write("TLSSYNC1");
    OSA.write("ATREF1");
    OSA.write("STAWL" + str(Swp_Start));
    OSA.write("STPWL" + str(Swp_End));
    OSA.write("AVG" + str(Ave_rpts));
    OSA.write("SMPL" + str(Samples));
    OSA.write("SHI" + str(Sensitivity))
    return 

def swp_start(TLS,OSA):
    TLS.write("L1")
    OSA.write("SGL")
    return

def go2local(TLS,OSA):
    TLS.ibloc()
    OSA.ibloc()
    return

def save(TLS,OSA,Filename):                               
    OSA.write("WDATA R1-R20001");           #Command to retrive data.
    Raw_Lam1 = OSA.read(18000);             #command to read data.
    Raw_Lam2 = Raw_Lam1.decode('UTF-8');    #data is decoded as a string.
    Raw_Lam3 = Raw_Lam2.split(',');         #converted to a list.
    Lambda = np.double(Raw_Lam3[2:-1]);        #converted to a numpy array.
    OSA.write("LDATA R1-R20001");           #same again....
    Raw_int1 = OSA.read(18000);
    Raw_int2 = Raw_int1.decode('UTF-8');
    Raw_int3 = Raw_int2.split(',');    
    Intensity = np.double(Raw_int3[2:-1]);
    Intensity = Intensity[0:np.size(Lambda)];
    np.savetxt("data/" + Filename + ".txt", (Intensity, Lambda), delimiter=',');
    print("text file saved in data folder")
    return
