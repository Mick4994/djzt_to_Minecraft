import numpy as np
import cv2

f = open('256.txt','r')
all_lines = f.readlines()
f.close()

value_list = []

for line in all_lines:
    rgb_index = line.index('rgb')
    rgb_end_index = rgb_index + line[line.index('rgb'):-1].index(')')
    value_str = [int(i) for i in line[rgb_index+4:rgb_end_index].split(',')]
    value_list.append(value_str)
print('value_list_len:',len(value_list))
# print(value_list)

def show_map():
    map_256 = np.reshape(np.array(value_list,dtype=np.uint8),(16,16,3))
    cv2.namedWindow('map',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('map',512,512)
    cv2.imshow('map',map_256)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

i = 0
for rgb in value_list:
    i += 1
    block_name = 'block_' + str(rgb[0]) + '_' + str(rgb[1]) + '_' + str(rgb[2]) + '.png'
    img = np.reshape(np.array(rgb, dtype=np.uint8),(1,1,3))
    cv2.imwrite('./texture256/' + block_name, img)
    print(i,':',block_name)