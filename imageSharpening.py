import numpy as np
import skimage
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import os
import scipy.misc as sm
from scipy.ndimage.filters import convolve
from skimage import color
from skimage.draw import circle
from matplotlib import patches

#Read and display the image to analyze
def load_img(filename):
    if os.path.isfile(os.getcwd() + '/' + filename):
        img = mpimg.imread(filename)
        return img
    return 0

#Create a Gaussian filter of n x n size and width sigma
def gaussian_filter(n, sigma=1):
    n = int(n) // 2
    x, y = np.mgrid[-n:n+1, -n:n+1]
    g =  (np.exp(-((x**2 + y**2) / (2.0*sigma**2)))) / (2.0 * np.pi * sigma**2)
    return g
 

#draw a circular patch on a color image Img; the patch is centered at r,c, with radius rad
#and color col (0-black; 1-red; 2-cyan; 3-green)
#Note that this function directly modifies Img. 
def draw_patch(Img, r, c, rad=7,col=1):   
    if col == 2:
        p = [0,1.0,1.0] #cyan
    else:
        p = [0,1.0,0.0] #green
    if col == 1: 
        p = [1.0,0.0,0.0]#red
    if col == 0: 
        p = [0.0,0.0,0.0]#black
        
    rr, cc = skimage.draw.circle(r, c, rad)
    Img[rr,cc, 0:3]= p       
    
folder_Path = 'images/'
file1 = 'timnit_blur.jpg'


#1. Load your image of choice.
firstFile = folder_Path + file1
img = load_img(firstFile)

#2. Create a Gaussian filter here
g = gaussian_filter(30,sigma=2)

#3. Next, convert your image to L.a.b. color scale
lab = color.rgb2lab(img)

#4. Extract the first channel to get the intensity-only image. Say this results in L
L = lab[:,:,0]


#5. Convolve this new image L with the filter g to get a smoothed image Simg
Simg = convolve(L,g)
               
#6. Create a new image by multiplying L by a small constant r and Simg by another small constant s
r = 0.6
s = 0.5
newL = r*L - s*Simg

#7. Normalize your new image so that its values are between 0 and 100
normL = 100*(newL - newL.min())/(newL.max() - newL.min())

#8. Recombine this new L image with the previous a and b channels of the lab image in step #3.
lab[:,:,0] = normL

#9. Reconvert the L.a.b. image back to RGB with the command below (assuming the new L.a.b. image is called lab2)
img2 = skimage.color.lab2rgb(lab)

#10. Examine your newly sharpened image and save it to file. Also display the original and sharpened image side-by-side

fig = plt.figure()
fig.add_subplot(1,2,1)
plt.imshow(img)
fig.add_subplot(1,2,2)
plt.imshow(img2)
