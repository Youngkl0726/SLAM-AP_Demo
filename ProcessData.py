import matplotlib.pyplot as plt
#
# def get_camera_traj(filename):
#     x_p = []
#     y_p = []
#     camera_traj = [[] for i in range(500)]
#     camera_file = open(filename)
#     id = -1
#     cnt = 0
#     flag = 0
#     num_r = 0
#     line = ""
#     for i in range(14454):
#         camera_line = camera_file.readline()
#         camera_line = camera_line.strip()
#         li = camera_line.split(" ")
#         # print camera_line[0]
#         if camera_line[0] == 'T':
#             id += 1
#             num_r = 0
#             if flag == 1:
#                 camera_traj[id].append(camera_traj[id-1][0])
#                 x_p.append(x_p[id-1])
#                 y_p.append(y_p[id-1])
#         if camera_line[0] == 'R':
#             if num_r == 1:
#                 continue
#             flag = 1
#             if id != 0:
#                 camera_traj[id].pop()
#                 x_p.pop()
#                 y_p.pop()
#             # print camera_line
#             camera_line = camera_line.split(" ")
#             # print camera_line
#             camera_traj[id].append(camera_line[1:])
#             x = float(li[4])
#             y = float(li[12])
#             x_p.append(x)
#             y_p.append(y)
#             num_r = 1
#             # if flag == 1:
#             #     continue
#             # # camera_traj[i].append(camera_line[1:])
#             # for j in range(id, id-cnt, -1):
#             #     camera_traj[j].append(camera_line[1:])
#             # cnt = 0
#             # # print camera_traj[i]
#             # flag = 1
#     return camera_traj, x_p, y_p
#
#
# filename = 'slamout.txt'
# camera_traj, x_p, y_p = get_camera_traj(filename)
# print camera_traj
# print x_p, y_p
# print len(x_p), len(y_p)
# sleep_t = 0.001
# for i in range(500):
#     fig1 = plt.figure(1)
#     plt.pause(sleep_t)
#     plt.clf()
#     plt.axis([-50, 200, -400, 50])
#     plt.scatter(x=x_p[i], y=y_p[i], marker='o')
#     plt.plot(x_p[0:], y_p[0:])
# plt.show()
def get_camera_traj(filename):
    x_p = []
    y_p = []
    camera_file = open(filename)
    id = -1
    cnt = 0
    flag = 0
    num_r = 0
    line = ""
    for i in range(14875):
        camera_line = camera_file.readline()
        camera_line = camera_line.strip()

        # print camera_line
        # print camera_line[0]
        if camera_line[0] == 'T':
            id += 1
            num_r = 0
            if flag == 1:
                x_p.append(x_p[id-1])
                y_p.append(y_p[id-1])
        if camera_line[0] == 'O':
            if num_r == 1:
                continue
            flag = 1
            if id != 0:
                x_p.pop()
                y_p.pop()
            camera_line = camera_line.split(" ")
            x = float(camera_line[1])
            y = float(camera_line[3])
            x_p.append(x)
            y_p.append(y)
            num_r = 1
    # print x_p
    # print y_p
    return x_p, y_p

slam_O_file = r'./sz_time/slam_O.txt'
x_p, y_p = get_camera_traj(slam_O_file)

sleep_t = 0.001
for i in range(500):
    fig1 = plt.figure(1)
    plt.pause(sleep_t)
    plt.clf()
    plt.axis([-50, 200, 0, 300])
    plt.scatter(x=x_p[i], y=y_p[i], marker='o')
    plt.plot(x_p[0:], y_p[0:])
plt.show()