import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path

file_dir = '/Users/youngkl/Desktop/Demo/image_0/'
x = []
y = []
for i in range(10):
    x.append(i*100)
    y.append(i*30)

plt.figure()
SLEEP_T = 0.1
for i in range(10):
    plt.pause(SLEEP_T)
    plt.clf()
    plt.axis([0, 1250, 350, 0])
    image_name = '{:0>6d}.png'.format(i)
    img = mpimg.imread(path.join(file_dir, image_name))
    # print img
    plt.imshow(img, cmap='gray')
    plt.scatter(x=x[0:], y=y[0:], c='r', marker='o')
plt.show()
