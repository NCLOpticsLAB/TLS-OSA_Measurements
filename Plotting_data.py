
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:30:24 2018

@author: chriscrossing
"""
import numpy as np
import Functions
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


Filenames = Functions.load_obj('Filenames')
Common_default = Functions.load_obj('Common_default')



while True:
    print("Attatched data")
    print("")
    question = input("> ")
    
    if question == '':
        break
    else:
        newFilenames = {
        'Filename1': question
        }
        Filenames.update(newFilenames)
        Functions.save_obj(Filenames, 'Filenames')
        break

while True:
    print("Detached data")
    print("")
    question = input("> ")
    if question == '':
        break
    else:
        newFilenames = {
        'Filename2': question
        }
        Filenames.update(newFilenames)
        Functions.save_obj(Filenames, 'Filenames')
        break




while True:
    print("Start sweep wavelength (leave blank to read last sweep value")
    print("")
    Swp_Start = input("> ")
    if Swp_Start == '':
        Swp_Start = Common_default.get('Swp_Start')
        break     
    else:
        break

while True:
    print("End sweep wavelength (leave blank to read last sweep value")
    print("")
    Swp_End = input("> ")
    if Swp_End == '':
        Swp_End = Common_default.get('Swp_End')
        break     
    else:
        break
    
while True:
    print("Figure name")
    print("")
    Figurename = input("(leave blank to not save)> ")   
    if Figurename == '':
        save = False
        break
    else:
        save = True
        break    


(Intensity1,Lambda) = np.loadtxt("Data/" + Filenames.get('Filename1') + ".txt", delimiter=',')
(Intensity2,Lambda1) = np.loadtxt("Data/" + Filenames.get('Filename2') + ".txt", delimiter=',')



Intensity1 = Intensity1[Lambda < float(Swp_End)]
Intensity2 = Intensity2[Lambda < float(Swp_End)]
Lambda = Lambda[Lambda < float(Swp_End)]

Losses = Intensity2 - Intensity1

#Removing the zero values.

#Lambda_fit = Lambda[Losses > 0]
#Losses_fit = Losses[Losses > 0]


p,cov = np.polyfit(Lambda,Losses,1,cov=True)

#errors

cov_p = np.sqrt(np.diag(cov))
m = cov_p[0]
c = cov_p[1]

y_err = m*Lambda +c 



#Plotting the graph
f, ax = plt.subplots(1,figsize=(17,6))

#Figure Formatting
plt.xlabel('Wavelength / nm', fontsize=30);
plt.ylabel('Losses / dBm', fontsize=30);
plt.ylim([0,np.max(y_err)+np.max(Losses)])
plt.xlim([float(Swp_Start),float(Swp_End)])
Ave_Error = np.average(y_err)
Ave_Losses = np.average(Losses[Losses != 0])
Losses_text = "Average Losses: " + str(np.round(Ave_Losses,4)) + " $\pm$" + str(np.round(Ave_Error,4)) + " dBm"
plt.title(Losses_text, fontsize=20);
plt.tight_layout()

#Plot the Losses of the fiber device
ax.scatter(Lambda, Losses,marker='x')

#Now a linear fit.
ax.plot(Lambda, np.polyval(p,Lambda),color='green',linewidth=2)

#And now the two upper and lower errors.
ax.plot(Lambda,y_err+np.polyval(p,Lambda),':',color='red',linewidth=3)
ax.plot(Lambda,np.polyval(p,Lambda)-y_err,':',color='red',linewidth=3)

#Below is for the Key.
Red_Patch = mpatches.Patch(color='red', label='Error')
Blue_Patch = mpatches.Patch( label='Data Points')
Green_Patch = mpatches.Patch(color='green', label='Linear fit')
plt.legend(handles=[Blue_Patch,Green_Patch,Red_Patch],fontsize=20)

plt.show()

while True:  
    if save == True:
        print('Figure saved as ' + Figurename)
        plt.savefig("figures/" + Figurename +  ".eps", format='eps', dpi=600);
        break
    else:
        print('Figure not saved!!!')
        break

