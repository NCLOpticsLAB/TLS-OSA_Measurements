#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:08:22 2018

@author: chriscrossing
"""

Common = {
        'Swp_Start': 1520.000,          #nanometers 1520-1620 nm
        'Swp_End': 1575.000,            #---------//-----------
        }

TLS = {
        'adr': 1,        
        'Swp_Step': "TSTEWL%f"  %0.2,   #TLS 0.001-100 nm must be less than half OSA-res.
        'Swp_Time': "TSWET%f"   %3,     #0-99999 s
        'Stp_Time': "TSTET%f"   %3,     #0.1-999 s
        'Power': "TPMW%f"    %2,        #milliwatts max = 6 mW  
        'Ave_Times': "AVG%f" %8,          
        'Wavelength': "TWL%f" %1570.000 #Low to high; SNHD SNAT SMID SHI(1-3).
        }

OSA = {
       'adr': 2,
       'Resolution': "RESOLN%f"  %0.5, #OSA nanometers, 0.01nm-2nm
       'Samples': "SMPL%f" %400,       #Minimum = no. of divisions (Wavelength range / Resoloution)
       'Sensitivity': "SHI2",          #Low to high; SNHD SNAT SMID SHI(1-3)
       }
