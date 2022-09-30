#Afficher le circuit
##

#%%
import matplotlib.pyplot as plt
import numpy as np

plt.clf()
a=np.array([2.,3.])
b=np.array([5.,4.])
c=np.array([5.,1.])
d=np.array([1.,1.])

points=[[a,0.5],[b,0.2],[c,0.5],[d,0.1]]

circuit=[[0.3217505543966423,
 2.7225148226554414,
 (0.2, 1.892546881191539),
 3.5,
 (0.5, 1.5707963267948966),
 3.8381966011250106,
 (0.1, 2.0344439357957027),
 2.0289611963132423,
 (0.5, 0.7853981633974484)]

for i,(point,_) in enumerate(points):
    print(point)
    plt.scatter(point[0],point[1])


def droite(point,long,angle):
    x=point[0]+long*np.cos(angle)
    y=point[1]+long*np.sin(angle)
    return np.array([x,y])
    
pos=points[0][0]
angle=circuit[0]
for move in circuit[1:]:
    if type(move)==float:
        pos1=droite(pos,move,angle)
        plt.plot(pos,pos1)
        pos=pos1
    else:
        angle+=move[1]


    

plt.show()



# %%
