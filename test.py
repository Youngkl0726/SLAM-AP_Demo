import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np
import cv2

bf = 379.8145
fx = 707.0912
fy = 707.0912
cx = 601.8873
cy = 183.1104
invfx = 1.0 / fx
invfy = 1.0 / fy
# print invfx, invfy

# sleep_t = 0.1
# for i in range(271):
#     # figure = plt.figure()
#     # plt.pause(sleep_t)
#     # plt.clf()
#     ori_img_dir = './Demo04/image_0/'
#     disp_img_dir = './kitti_disp_gen/04/'
#     seg_img_dir = './Demo04/ideal_result/'
#     image_name = '{:0>6d}.png'.format(i)
#     ori_img = cv2.imread(path.join(ori_img_dir, image_name))
#     disp_img = np.array(Image.open(path.join(disp_img_dir, image_name)))/256
#     depth_img = bf / disp_img
#     print depth_img.max()
#     m = depth_img.max()
#     if m > 100:
#         print i
#     seg_img = np.array(Image.open(path.join(seg_img_dir, image_name)))
#     # for j in range(370):
#     #     for k in range(1226):
#     #         if seg_img[j][k] == 255:
#     #             seg_img[j][k] = 100
#     #         ori_img[j][k][0] += seg_img[j][k]
#     #         ori_img[j][k][0] %= 256
#     # plt.imshow(ori_img, cmap='gray')
#     # plt.show()

ori_img = cv2.imread('./Demo04/image_0/000000.png')
h,w,c = ori_img.shape
print h,w,c
# print ori_img.shape
disp_img = np.array(Image.open('./kitti_disp_gen/04/000000.png'))/256
depth_img = bf / disp_img
print depth_img.max(), depth_img.min()
print depth_img.shape
seg_img = np.array(Image.open('./Demo04/ideal_result/000000.png'))
print seg_img.shape
for j in range(370):
    for k in range(1226):
        if seg_img[j][k] == 255:
            # seg_img[j][k] = 100
            for m in range(3):
                ori_img[j][k][m] = 255
        # ori_img[j][k][0] += seg_img[j][k]
        # ori_img[j][k][0] %= 256
# m = depth_img.max()
# for j in range(370):
#     for k in range(1226):
#
#         ori_img[j][k][0] = ori_img[j][k][0]*0.2 + 2 * (m-depth_img[j][k])
#         ori_img[j][k][1] *= 0.2
#         ori_img[j][k][2] *= 0.2
figure = plt.figure()
plt.clf()
plt.imshow(ori_img, cmap='gray')
plt.show()



# def get_3d_wcor(u, v, z, rwc, ow):
#     x = (v - cx) * z * invfx
#     y = (u - cy) * z * invfy
#     x3dc = [[] for k in range(3)]
#     x3dc[0].append(x)
#     x3dc[1].append(y)
#     x3dc[2].append(z)
#     mat_3dc = np.mat(x3dc)
#     mat_res = rwc.dot(mat_3dc) + ow
#     # print mat_res[0][0], mat_res[2][0]
#     list_res = mat_res.tolist()
#     return list_res
#
#
# def get_camera_traj(filename):
#     camera_file = open(filename)
#     x_p = []
#     y_p = []
#     camera_traj = [[] for i in range(1801)]
#     for i in range(271):
#         camera_line = camera_file.readline()
#         camera_line = camera_line.strip()
#         camera_line = camera_line.split(" ")
#         camera_traj[i].append(camera_line)
#         x = float(camera_line[3])
#         y = float(camera_line[11])
#         x_p.append(x)
#         y_p.append(y)
#     camera_file.close()
#     return camera_traj, x_p, y_p
#
# camera_file = r'./Demo04/CameraTrajectory.txt'
# camera_traj, camera_x, camera_y = get_camera_traj(camera_file)
#
# sleep_t = 0.001
# for i in range(271):
#     fig1 = plt.figure(1)
#     plt.pause(sleep_t)
#     plt.clf()
#     plt.axis([-100, 300, -100, 500])
#     camera_t = camera_traj[i]
#     camera = camera_t[0]
#     r = [[] for k in range(3)]
#     for k in range(3):
#         for j in range(3):
#             r[k].append(float(camera[j + k * 4]))
#     mat_r = np.mat(r)
#     t = [[] for k in range(3)]
#     for k in range(3):
#         t[k].append(float(camera[3 + k * 4]))
#     mat_t = np.mat(t)
#     rwc = mat_r.transpose()
#     ow = (-rwc).dot(mat_t)
#     # Get depth map
#     img_dir = './kitti_disp_gen/04/'
#     img_name = '{:0>6d}.png'.format(i)
#     image_dir = path.join(img_dir, img_name)
#     img = np.array(Image.open(image_dir))
#     img = img / 256
#     img_depth = bf / img
#
#     road_left_curr_3dx = []
#     road_left_curr_3dy = []
#     road_right_curr_3dx = []
#     road_right_curr_3dy = []
#     seg_img_dir = './Demo04/ideal_result/'
#     seg_image_dir = path.join(seg_img_dir, img_name)
#     seg_img = np.array(Image.open(seg_image_dir))
#     h = seg_img.shape[0]
#     w = seg_img.shape[1]
#     uleft = 0
#     vleft = 0
#     uright = 0
#     vright = 0
#     # print seg_img
#     # for j in range(h):
#     #     flag = 0
#     #     for k in range(w):
#     #         if seg_img[j][k]==0:
#     #             flag=1
#     #     if flag == 0:
#     #         print i, j
#     for j in range(h - 1, -1, -1):
#         for k in range(w):
#             if seg_img[j][k] == 255:
#                 # print "j is: ", j, "k is: ",k
#                 uleft = j
#                 vleft = k
#                 break
#         for k in range(w - 1, -1, -1):
#             if seg_img[j][k] == 255:
#                 # print "j is: ", j, "k is: ", k
#                 uright = j
#                 vright = k
#                 break
#         # print uleft, vleft
#         zleft = -img_depth[uleft][vleft]
#         left_res = get_3d_wcor(uleft, vleft, zleft, rwc, ow)
#         # print left_res
#         zright = -img_depth[uright][vright]
#         right_res = get_3d_wcor(uright, vright, zright, rwc, ow)
#         road_left_curr_3dx.append(-left_res[0][0])
#         road_left_curr_3dy.append(-left_res[2][0])
#         road_right_curr_3dx.append(-right_res[0][0])
#         road_right_curr_3dy.append(-right_res[2][0])
#     plt.plot(road_left_curr_3dx[0:], road_left_curr_3dy[0:], c='black')
#     plt.plot(road_right_curr_3dx[0:], road_right_curr_3dy[0:], c='darkcyan')
#     print "size is: ", len(road_left_curr_3dx)
#     if len(road_left_curr_3dx) != 370:
#         print i
#         break
#     print road_left_curr_3dx
#     print road_left_curr_3dy

