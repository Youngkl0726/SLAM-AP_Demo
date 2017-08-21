import matplotlib.pyplot as plt


camera_file = open("CameraTrajectory.txt")
slam2 = open("slam_out2.txt")
ap_file = open("ap_out.txt")

x_p = []
y_p = []
for i in range(1801):
    camera_line = camera_file.readline()
    camera_line = camera_line.strip()
    camera_line = camera_line.split(" ")
    x = float(camera_line[3])
    y = float(camera_line[11])
    x_p.append(x)
    y_p.append(y)

slam_3D_pos = [[] for i in range(1801)]
slam_pic_pos = [[] for i in range(1801)]
slam_num = -1
for i in range(414764):
    slam_line = slam2.readline()
    slam_line = slam_line.strip()
    # print slam_line
    if slam_line[0] == 'T':
        slam_num = slam_num + 1
        # print slam_num
        continue
    if slam_line[0] == 'C':
        continue
    if slam_line[0] == '(':
        slam_pic_pos[slam_num].append(slam_line[1:-1])
    else:
        slam_3D_pos[slam_num].append(slam_line)
slam2.close()

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

print len(x_p)

SLEEP_T = 0.01
fig1 = plt.figure(1)
fig2 = plt.figure(2)
for i in range(1801):

    fig1 = plt.figure(1)
    plt.pause(SLEEP_T)
    plt.clf()
    plt.axis([-300, 600, -100, 600])
    plt.plot(x_p[0:i], y_p[0:i])
    point_x = []
    point_y = []
    for line in (slam_3D_pos[i]):
        line = line.split(' ')
        x = float(line[0])
        y = float(line[1])
        point_x.append(x)
        point_y.append(y)
    plt.scatter(x=point_x[0:], y=point_y[0:], c='r', marker='o')

    fig2 = plt.figure(2)
    plt.axis([0, 1250, 0, 400])
    plt.pause(SLEEP_T)
    plt.clf()

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
        # print (p1, p2, p3, p4)
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='black')
        plt.plot([p1[0], p3[0]], [p1[1], p3[1]], c='black')
        plt.plot([p4[0], p2[0]], [p4[1], p2[1]], c='black')
        plt.plot([p4[0], p3[0]], [p4[1], p3[1]], c='black')
        # for j in range(slam_len):
        #     x = pic_x[j]
        #     y = pic_y[j]
        #     if x - left > 0.0000001 and right - x < 0.0000001 and y - top > 0.0000001 and bottom - y > 0.0000001:
        #         cnt = cnt + 1
        #         cor_x.append(x)
        #         cor_y.append(y)
    plt.scatter(x=pic_x[0:], y=pic_y[0:], c='r', marker='o')

plt.show()
