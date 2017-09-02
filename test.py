from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img=np.array(Image.open('/Users/youngkl/Desktop/Demo/kitti_disp_gen/18/000385.png'))
print img/256
