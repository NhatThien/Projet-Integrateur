from time import time
import numpy as np
import matplotlib.pyplot as plt
import sys

t1=time()
array_reloaded = np.load(sys.argv[1])
t2=time()

image = array_reloaded*20
print('\nShape: ',array_reloaded.shape)
print('\nShape: ',array_reloaded)
print(f"Time took to load: {t2-t1} seconds.")
#print(array_reloaded)
print("max", np.amax(image))

'''
plt.figure()
plt.imshow(image)
plt.show()
'''