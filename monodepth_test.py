import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
import numpy as np
from PIL import Image
import cv2

# def convert_disps_to_depths_kitti(pred_disparities):
#     gt_depths = []
#     pred_depths = []
#     pred_disparities_resized = []
#
#     for i in range(len(pred_disparities)):
#         pred_disp = pred_disparities[i]
#         height, width = pred_disp.shape
#         pred_disp = width * cv2.resize(pred_disp, (width, height), interpolation=cv2.INTER_LINEAR)
#
#         pred_disparities_resized.append(pred_disp)
#         pred_depth = 512 * 0.54 / pred_disp
#         pred_depths.append(pred_depth)
#     return pred_depths
#
#
# disp_image_dir = ('./monodepth/001143_disp.png')
# disp_img = np.array(Image.open(disp_image_dir))
# pred_depths = convert_disps_to_depths_kitti(disp_img)


# print pred_depths.shape
# print pred_depths[401][283]

disp_image_dir = ('./monodepth/disparities_pp4.npy')
disp = np.load(disp_image_dir)
print disp.shape


def get_ap_log(filename):
    file = open(filename)
    res_line = [[] for i in xrange(5906)]
    for i in xrange(5906):
        # print i
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        # print len(line)
        # print line
        res_line[i].append(int(line[0]))
        res_line[i].append(int(line[1]))
        res_line[i].append(float(line[6]))
        res_line[i].append(float(line[7]))
        res_line[i].append(float(line[8]))
        res_line[i].append(float(line[9]))
        # res_line[i].append(float(line[18]))
        # res_line[i].append(float(line[19]))
        # res_line[i].append(float(line[20]))
        # res_line[i].append(float(line[21]))
    # print res_line
    return res_line

bf = 33.0

def draw(ap_res):
    depth = []
    depth_id = []
    depth_num = 0
    sleep_t = 0.001
    for i in xrange(824):
        if i==823:
            plt.plot(depth_id[0:], depth[0:], c='blue')
        # print ap_res[i]
        # Get depth map
        person_id = ap_res[i][1]
        if person_id != 8:
            continue
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        pic_id = ap_res[i][0]
        disp_i = cv2.resize(disp[pic_id], (878, 493), interpolation=cv2.INTER_LINEAR)
        depth_img = bf / (disp_i * 512.0)
        point1_x = ap_res[i][2]
        point1_y = ap_res[i][3]
        point2_x = ap_res[i][4]
        point2_y = ap_res[i][5]
        mid_x = int((point1_x + point2_x) / 2)
        mid_y = int((point1_y + point2_y) / 2)
        mid_x = min(493, mid_x)
        mid_y = min(878, mid_y)

        z = depth_img[mid_y][mid_x]
        if z > 30:
            continue

        depth.append(z)
        depth_id.append(depth_num)
        depth_num += 1
        plt.plot(depth_id[0:], depth[0:], c='blue')
    plt.pause(10)
    plt.show()

def main():
    ap_file = r'./monodepth/r_4_out.log'
    ap_res = get_ap_log(ap_file)
    draw(ap_res)


if __name__ == '__main__':
    main()
