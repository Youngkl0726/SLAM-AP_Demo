from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

bf = 386.1448
fx = 718.856
fy = 718.856
cx = 607.1928
cy = 185.2157
invfx = 1.0/fx
invfy = 1.0/fy
# print invfx, invfy

img = np.array(Image.open('/Users/youngkl/Desktop/Demo/kitti_disp_gen/18/000000.png'))
# print img
img = img/256

depth = bf/img
# print depth[100][100]
# print depth

def get_camera_traj(filename):
    camera_file = open(filename)
    x_p = []
    y_p = []
    camera_traj = [[] for i in range(10)]
    for i in range(10):
        camera_line = camera_file.readline()
        camera_line = camera_line.strip()
        camera_line = camera_line.split(" ")
        cam = []
        for j in range(12):
            cam.append(float(camera_line[j]))
        cam.append(0.0)
        cam.append(0.0)
        cam.append(0.0)
        cam.append(1.0)
        r = [[] for k in range(4)]
        for k in range(4):
            for j in range(4):
                r[k].append(float(cam[j+k*4]))
        # print r
        mat_r = np.mat(r)
        # print mat_r
        print mat_r.I
        # print mat_r.dot(mat_r.I)
        # print mat_r.transpose()
        # print camera_line

        camera_traj[i].append(camera_line)
        # print camera_traj
        x = float(camera_line[3])
        y = float(camera_line[11])
        x_p.append(x)
        y_p.append(y)
    camera_file.close()
    # print camera_traj
    return x_p, y_p

camera_f = r'./Demo00/CameraTrajectory.txt'
get_camera_traj(camera_f)
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         print img[i][j],
#     print ""

