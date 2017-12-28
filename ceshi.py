import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np

disp_img_dir = './Stereo/disp/'
img_name = '{:0>6d}.png'.format(0)
disp_image_dir = path.join(disp_img_dir, img_name)
disp_img = np.array(Image.open(disp_image_dir))
print disp_img[100][100]