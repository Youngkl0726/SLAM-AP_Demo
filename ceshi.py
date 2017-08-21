import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path

file_dir = '/Users/youngkl/Desktop/Demo/image_0/'
xx = []
yy = []
for i in range(10):
    xx.append(i*10)
    yy.append(i*30)


left = 55
right = 75
top = 75
bottom = 195
p1 = []
p2 = []
p3 = []
p4 = []
p1.append(left)
p1.append(top)
p2.append(right)
p2.append(top)
p3.append(left)
p3.append(bottom)
p4.append(right)
p4.append(bottom)
plt.figure()
plt.axis([0, 150, 0, 400])
plt.scatter(x=xx[:], y=yy[:], c='b', marker='o')
plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='green')
plt.plot([p1[0], p3[0]], [p1[1], p3[1]], c='green')
plt.plot([p4[0], p2[0]], [p4[1], p2[1]], c='green')
plt.plot([p4[0], p3[0]], [p4[1], p3[1]], c='green')

cor_x = []
cor_y = []
for i in range(10):
    x = xx[i]
    y = yy[i]
    print x, y
    print x - left, right - x, y - top, bottom - y
    print x - left > 0, right - x > 0, y - top > 0, bottom - y > 0
    if x - left > 0 and right - x > 0 and y - top > 0 and bottom - y > 0:
        cor_x.append(x)
        cor_y.append(y)
print len(cor_x)
plt.scatter(x=cor_x[:], y=cor_y[:], c='r', marker='o')
plt.show()
