import matplotlib.pyplot as plt

camera_file = open("camera_pose.txt")
ap_file = open("ap_out.txt")
slam_file = open("slam_out.txt")
slam2 = open("slam_out2.txt")
point = []

# Save the coordinate of the camera
x_p = []
y_p = []

# for i in range(1801):
#     camera_line = camera_file.readline()
#     camera_line = camera_line.strip()
#     camera_line = camera_line.split(" ")
#     x = float(camera_line[0])
#     y = float(camera_line[1])
#     # print x, y
#     x_p.append(x)
#     y_p.append(y)
#     point.append(camera_line)
# camera_file.close()

# print len(x_p)
# print y_p

# for i in range(221):
#     fig = plt.figure()
#     ax1 = fig.add_subplot(111)
#     ax1.set_title('Scatter Plot')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     ax1.scatter(x=x_p[:i], y=y_p[:i], c='r', marker='o')
#     plt.legend('x1')
#     plt.show()
#     # fig.pause(SLEEP_T)
#     fig.close('all')

slam_3D_pos = [[] for i in range(1801)]
slam_pic_pos = [[] for i in range(1801)]
slam_num = -1

# for i in range(422175):
#     slam_line = slam_file.readline()
#     slam_line = slam_line.strip()
#     # print slam_line
#     if slam_line[0] == 'T':
#         slam_num = slam_num + 1
#         # print slam_num
#         continue
#     if slam_line[0] == '(':
#         slam_pic_pos[slam_num].append(slam_line[1:-1])
#     else:
#         slam_3D_pos[slam_num].append(slam_line)
# slam_file.close()

for i in range(414764):
    slam_line = slam2.readline()
    slam_line = slam_line.strip()
    # print slam_line
    if slam_line[0] == 'T':
        slam_num = slam_num + 1
        # print slam_num
        continue
    if slam_line[0] == 'C':
        slam_line = slam_line.split(' ')
        x = float(slam_line[3])
        y = float(slam_line[4])
        x_p.append(x)
        y_p.append(y)
        continue
    if slam_line[0] == '(':
        slam_pic_pos[slam_num].append(slam_line[1:-1])
    else:
        slam_3D_pos[slam_num].append(slam_line)
slam2.close()
# print slam_3D_pos
# print slam_num

ap_num = -1
ap_pos = [[] for i in range(1801)]
for i in range(9538):
    ap_line = ap_file.readline()
    ap_line = ap_line.strip()
    if ap_line[0] == 's':
        ap_num = ap_num + 1
        # print ap_num
    else:
        ap_pos[ap_num].append(ap_line)
ap_file.close()

SLEEP_T = 0.01
fig = plt.figure()
for i in range(1801):
    plt.pause(SLEEP_T)
    plt.clf()
    plt.axis([-300, 600, -600, 600])
    plt.plot(x_p[:i], y_p[:i])
    point_x = []
    point_y = []
    for line in (slam_3D_pos[i]):
        line = line.split(' ')
        x = float(line[0])
        y = float(line[1])
        point_x.append(x)
        point_y.append(-1*y)

    pic_x = []
    pic_y = []
    for line in (slam_pic_pos[i]):
        line = line.split(' ')
        x = float(line[0])
        y = float(line[1])
        pic_x.append(x)
        pic_y.append(y)

    ap_left = []
    ap_top = []
    ap_right = []
    ap_bottom = []
    if len(ap_pos[i]) == 0:
        continue
    for line in (ap_pos[i]):
        line = line.split(' ')
        left = float(line[0])
        top = float(line[1])
        right = float(line[2])
        bottom = float(line[3])
        ap_left.append(left)
        ap_top.append(top)
        ap_right.append(right)
        ap_bottom.append(bottom)

    ap_len = len(ap_left)
    slam_len = len(point_x)
    cor_x = []
    cor_y = []
    cnt = 0
    for k in range(ap_len):
        left = ap_left[k] - 10
        top = ap_top[k] - 10
        right = ap_right[k] + 10
        bottom = ap_bottom[k] + 10
        for j in range(slam_len):
            x = pic_x[j]
            y = pic_y[j]
            if x-left>0.0000001 and right-x<0.0000001 and y-top>0.0000001 and bottom-y>0.0000001:
                cnt = cnt+1
                cor_x.append(x_p[i]+point_x[j])
                cor_y.append(y_p[i]+point_y[j])
    print i, cnt
    print cor_x
    print cor_y
    plt.scatter(x=point_x[0:], y=point_y[0:], c='r', marker='o')
plt.show()
