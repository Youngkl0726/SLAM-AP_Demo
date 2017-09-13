import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np
import cv2

def get_ap_info(filename):
    ap_file = open(filename)
    ap_num = -1
    ap_pos = [[] for i in range(271)]
    for i in range(787):
        ap_line = ap_file.readline()
        ap_line = ap_line.strip()
        if ap_line[0] == 's':
            ap_num = ap_num + 1
            # print ap_num
        else:
            ap_pos[ap_num].append(ap_line)
    ap_file.close()
    return ap_pos

def draw_points(ap_pos):
    sleep_t = 0.001
    for i in range(271):
        print "i is : ", i
        image_name = '{:0>6d}.png'.format(i)
        bv_dir = './SaveResults/04/'
        disp_img_dir = './kitti_disp_gen/04/'
        seg_img_dir = './SaveResults/seg04/'
        # seg_img_dir = './Demo04/ideal_result/'
        ori_img_dir = './Demo04/image_0/'

        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        bv_img = mpimg.imread(path.join(bv_dir, image_name))
        plt.axis('off')
        plt.title('birdview')
        plt.imshow(bv_img)

        fig2 = plt.figure(2)
        plt.pause(sleep_t)
        plt.clf()
        ori_img = mpimg.imread(path.join(ori_img_dir, image_name))
        plt.imshow(ori_img, cmap='gray')
        ap_left = []
        ap_top = []
        ap_right = []
        ap_bottom = []
        for line in (ap_pos[i]):
            line = line.split(' ')
            left = float(line[1])
            top = float(line[2])
            right = float(line[3])
            bottom = float(line[4])
            ap_left.append(left)
            ap_top.append(top)
            ap_right.append(right)
            ap_bottom.append(bottom)
        ap_len = len(ap_top)
        for k in range(ap_len):
            left = ap_left[k]
            top = ap_top[k]
            right = ap_right[k]
            bottom = ap_bottom[k]
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
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='green')
            plt.plot([p1[0], p3[0]], [p1[1], p3[1]], c='green')
            plt.plot([p4[0], p2[0]], [p4[1], p2[1]], c='green')
            plt.plot([p4[0], p3[0]], [p4[1], p3[1]], c='green')
        plt.axis('off')
        plt.title('AP')

        fig3 = plt.figure(3)
        plt.pause(sleep_t)
        plt.clf()
        disp_img = mpimg.imread(path.join(disp_img_dir, image_name))
        plt.axis('off')
        plt.title('depth_image')
        plt.imshow(disp_img, cmap='gray')

        fig4 = plt.figure(4)
        plt.pause(sleep_t)
        plt.clf()
        seg_img = mpimg.imread(path.join(seg_img_dir, image_name))
        plt.axis('off')
        plt.title('seg_image')
        plt.imshow(seg_img, cmap='gray')
        # seg_img = np.array(Image.open(path.join(seg_img_dir, image_name)))
        # ori_img2 = cv2.imread(path.join(ori_img_dir, image_name))
        # for j in range(370):
        #     for k in range(1226):
        #         if seg_img[j][k] == 255:
        #             # seg_img[j][k] = 100
        #             for m in range(3):
        #                 ori_img2[j][k][m] = 255
        # plt.axis('off')
        # plt.imshow(ori_img2, cmap='gray')
        # fig4.savefig('./SaveResults/seg04/{:0>6d}.png'.format(i))

    plt.show()


def main():
    ap_file = r'./Demo04/ap04.txt'
    ap_pos = get_ap_info(ap_file)
    draw_points(ap_pos)


if __name__ == '__main__':
    main()
