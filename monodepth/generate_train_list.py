
txt_file = open('train.txt', 'wb')
for i in xrange(33061):
    left_file = 'image_0/' + '{:0>6d}.png'.format(i)
    # right_file = 'right/' + '{:0>6d}.png'.format(i)
    right_file = 'image_1/' + '{:0>6d}.png'.format(i)
    print left_file
    # txt_file.write(left_file+'\n')
    txt_file.write(left_file + ' ' + right_file + '\n')
txt_file.close()


# txt_file = open('finetune_list.txt', 'wb')
# for i in xrange(25058):
#     left_file = 'stillcar_0/image_0/' + '{:0>6d}.png'.format(i*2)
#     right_file = 'stillcar_0/image_1/' + '{:0>6d}.png'.format(i*2)
#     print left_file
#     txt_file.write(left_file + ' ' + right_file + '\n')
# for i in xrange(2896):
#     left_file = 'stillcar/image_0/' + '{:0>6d}.png'.format(i*2)
#     right_file = 'stillcar/image_1/' + '{:0>6d}.png'.format(i*2)
#     print left_file
#     txt_file.write(left_file + ' ' + right_file + '\n')
# txt_file.close()

# txt_file = open('final_20000.txt', 'wb')
# file = open('final.txt')
# for i in xrange(20000):
#     line = file.readline()
#     line = line.strip()
#     print line
#     txt_file.write(line+'\n')
# txt_file.close()
