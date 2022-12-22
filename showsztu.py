import open3d as o3d
import numpy as np
import os
import time

import cv2

# img = np.array([255,255,255])
# cv2.cvtColor(img,cv2.RGB)
start_time = time.time()

def show_source():
    print(get_runtime()+'loading pcd')
    all_pcd_file = os.listdir('3D-models/terra_pcd/')
    all_pcd_file = ['3D-models/terra_pcd/' + i for i in all_pcd_file if i.endswith('.pcd')]
    pcd_list = [o3d.io.read_point_cloud(pcd_file) for pcd_file in all_pcd_file]
    print('finished load')

    xyz_list = []
    color_list = []

    print(get_runtime()+'getting xyz and colors')
    count = 0
    for i in pcd_list:
        xyz_list += np.asarray(i.points).tolist()
        color_list += np.asarray(i.colors).tolist()
        count += 1
        print(get_runtime()+' get:',count)

    print(get_runtime()+'finish get, turning to array')

    xyz = np.array(xyz_list)
    colors = np.array(color_list)
    print(get_runtime()+'finish turn')

    sztu_pcd = o3d.geometry.PointCloud()
    sztu_pcd.points = o3d.utility.Vector3dVector(xyz)
    sztu_pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw([sztu_pcd])



def get_runtime() -> str:
    runtime = '{:.1f}'.format(time.time() - start_time)
    return 'runtime:'+ runtime + 's '

def forward():
    f = open('256.txt','r')
    all_lines = f.readlines()
    f.close()

    value_list = []

    for line in all_lines:
        rgb_index = line.index('rgb')
        rgb_end_index = rgb_index + line[line.index('rgb'):-1].index(')')
        value_str = [int(i) for i in line[rgb_index+4:rgb_end_index].split(',')]
        value_list.append(value_str)

    value_array = np.array(value_list, dtype=np.uint8)

    print(get_runtime()+'loading pcd')
    all_pcd_file = os.listdir('3D-models/terra_pcd/')
    all_pcd_file = ['3D-models/terra_pcd/' + i for i in all_pcd_file if i.endswith('.pcd')]
    pcd_list = [o3d.io.read_point_cloud(pcd_file) for pcd_file in all_pcd_file]
    # print('finished load')

    xyz_list = []
    color_list = []

    print(get_runtime()+'getting xyz and colors')
    count = 0
    for i in pcd_list:
        xyz_list += np.asarray(i.points).tolist()
        color_list += np.asarray(i.colors).tolist()
        count += 1
        print(get_runtime()+' get:',count)

    # print(get_runtime()+'finish get, turning to array')

    # xyz = np.array(xyz_list)
    # colors = np.array(color_list)
    # print(get_runtime()+'finish turn')

    int_xyz_dic = {}
    for i in range(len(xyz_list)):
        int_xyz_dic[str([int(xyz_list[i][0]),int(xyz_list[i][1]),int(xyz_list[i][2])])] = color_list[i]
        if i!= 0:
            print(get_runtime() + 'simplfing:{:.2f}%'.format(i*100/len(xyz_list)),'len int_xyz_dic/i:{:.2f}'.format(len(int_xyz_dic)/i), end='\r')
    print('\n',end='')

    int_xyz = []
    int_colors = []
    count = 0
    for key, value in int_xyz_dic.items():
        key = key[1:-1]
        a,b,c = key.split(',')
        int_xyz.append([int(a),int(b),int(c)])
        int_colors.append(value)
        count += 1
        print(get_runtime() + 'rebuild:{:.2f}%'.format(count*100/len(int_xyz_dic)), end='\r')
    print('\n',end='')
    np.save('int_xyz.npy',np.array(int_xyz))
    np.save('int_colors.npy',np.array(int_colors))
    print(get_runtime() + 'finish save numpy data')



def match_color():
    f = open('256.txt','r')
    all_lines = f.readlines()
    f.close()
    value_list = []

    for line in all_lines:
        rgb_index = line.index('rgb')
        rgb_end_index = rgb_index + line[line.index('rgb'):-1].index(')')
        value_str = [int(i) for i in line[rgb_index+4:rgb_end_index].split(',')]
        value_list.append(value_str)
    # colors = np.load('int_colors.npy')
    colors = np.load("match_colors_copy.npy")

    match_colors_list = []
    colors_255 = np.array(colors * 255, dtype = np.uint8)
    for i in range(len(colors_255)):
        diff_list = [sum([abs(value_list[j][k] - colors_255[i][k]) for k in range(len(value_list[j]))]) for j in range(len(value_list))]
        min_index = diff_list.index(min(diff_list))
        match_colors_list.append(np.array(value_list[min_index]))
        print(get_runtime()+'matching:{:.2f}'.format(i*100/len(colors_255)),"%",end='\r')
    print('\nfinish match')
    match_colors = np.array(match_colors_list)/255

    print(get_runtime()+'saving result')
    # f = open('match_colors.txt','w')
    f = open('match_colors_copy.txt','w')
    for i in range(len(match_colors_list)):
        f.write(str(match_colors_list[i]) + '\n')
        print(get_runtime()+'saving:{:.2f}'.format(i*100/len(match_colors_list)), end='\r')
    print('\n',end='')
    f.close()

    xyz = np.load('int_xyz.npy')
    return match_colors, xyz

def xyz_dis(sztu_pcd):
    x, y, z = zip(*np.asarray(sztu_pcd.points))
    print('x:',max(x)-min(x))
    print('y:',max(y)-min(y))
    print('z:',max(z)-min(z))

def save_colors_255():
    colors = np.load('int_colors.npy')
    colors_255 = np.array(colors * 255, dtype = np.uint8)
    f = open('colors_255.txt','w')
    count = 0
    for i in colors_255:
        f.write(str(i)+'\n')
        count += 1
        print(get_runtime() + 'save colors_255.txt:{:.2f}%'.format(count*100/len(colors_255)),end='\r')
    print('\n',end='')
    f.close()

def match_colors_copy_read():
    f = open('match_colors_copy.txt','r')
    all_lines = f.readlines()
    f.close()
    match_colors = []
    for i in all_lines:
        for j in range(len(i[1:-2])):
            if i[j] == ' ' and i[j+1] == ' ':
                i = i[0:j] + i[j+1:]
            elif i[j] == '[' and i[j+1] == ' ':
                i = i[0:j+1] + i[j+2:]
        num = [int(j) for j in i[1:-2].split(' ')]
        match_colors.append(num)
    # print(match_colors)
    match_colors = np.array(match_colors, dtype=np.uint8)
    return match_colors/255

def count_colors():
    match_colors = np.load('int_colors.npy')
    match_colors_list = match_colors.tolist()
    match_colors_dic = {}
    str_match_colors = []
    for i in range(len(match_colors_list)):
        str_key = str(match_colors_list[i])
        str_match_colors.append(str_key)
        match_colors_dic[str_key] = 0
    print(len(match_colors_dic))
    count = 0
    f = open('sort_count.txt','w')
    for key, value in match_colors_dic.items():
        match_colors_dic[key] = str_match_colors.count(key)
        # f.write(key + ':' + str(match_colors_dic[key]) + '\n')
        count += 1
        print(get_runtime() + 'save count.txt:{:.2f}%'.format(count*100/len(match_colors_dic)),end='\r')
    print('\n',end='')
    
    sort_count = sorted(match_colors_dic.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    print(sort_count)
    for i in sort_count:
        f.write(str(i) + '\n')
    f.close()

def turn_count_256():
    f = open('sort_count.txt','r')
    all_lines = f.readlines()
    f.close()
    f = open('sort_count_256.txt','w')
    count = 0
    for line in all_lines:
        line_copy = line
        line_copy = line_copy[line_copy.find('[')+1:line_copy.find(']')]
        f.write(str([int(float(i)*255) for i in line_copy.split(', ')]) + line[line.find(']') + 2:])
        count += 1
        print(get_runtime() + 'save turn_count_256.txt:{:.2f}%'.format(count*100/len(all_lines)),end='\r')
    print('\n',end='')
    f.close()

def to_10_dic_count(): #除十后统计颜色量
    f = open('sort_count_256.txt','r')
    all_lines = f.readlines()
    f.close()
    to_10_dic = {}
    count = 0
    for line in all_lines:
        line_copy = line
        line_copy = line_copy[line_copy.find('[')+1:line_copy.find(']')]
        key = str([int(i)//10*10 for i in line_copy.split(', ')])
        if key not in to_10_dic:
            to_10_dic[key] = int(line[line.find(']') + 3:-2])
        else:
            to_10_dic[key] += int(line[line.find(']') + 3:-2])
        count += 1
        print(get_runtime() + 'to_10_dic_count:{:.2f}%'.format(count*100/len(all_lines)),end='\r')
    print('\n',end='')
    print('len(to_10_dic):',len(to_10_dic))
    sort_count = sorted(to_10_dic.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    # f = open('sort_count_dic.txt','w')
    # count = 0
    # for key, value in to_10_dic.items():
    #     f.write(key + ":" + str(value) + '\n')
    #     count += 1
    #     print(get_runtime() + 'save sort_count_dic:{:.2f}%'.format(count*100/len(to_10_dic)),end='\r')
    # print('\n',end='')
    f = open('sort_count_dic.txt','w')
    for i in sort_count:
        f.write(i[0] + ':' + str(i[1]) + '\n')
    f.close()

def count_ahead256():
    f = open('match_colors.txt','r')
    len_dic = len(f.readlines())
    f.close()
    f = open('sort_count_dic.txt','r')
    all_lines = f.readlines()
    f.close()
    num = 0
    for i in range(1000):
        str_num = all_lines[i][all_lines[i].find(':') + 1: -1]
        num += int(str_num)
    print('256 in all colors:{:.3f}'.format(num/len_dic))

def match_count_colors():
    f = open('sort_count_dic.txt','r')
    all_lines = f.readlines()
    f.close()
    standard_value = []
    for i in range(256):
        line = all_lines[i]
        line = line[line.find('[') + 1:line.find(']')]
        r,g,b = line.split(', ')
        standard_value.append([int(r),int(g),int(b)])
    need_match_value = {}
    count = 0
    for i in range(256, len(all_lines)):
        line = all_lines[i]
        line = line[line.find('[') + 1:line.find(']')]
        r,g,b = line.split(', ')
        key = str([int(r),int(g),int(b)])
        diff_list = [abs(j[0] - int(r)) + abs(j[1] - int(g)) + abs(j[2] - int(b)) for j in standard_value]
        min_diff_index = diff_list.index(min(diff_list))
        need_match_value[key] = standard_value[min_diff_index]
        print(get_runtime() + 'matching:{:.2f}%'.format(count*100/(len(all_lines) - 256)),end='\r')
    print('\n',end='')
    f = open('need_match_value.txt','w')
    for key, value in need_match_value.items():
        f.write(str(key) + ':' + str(value) + '\n')
    f.close()

def show_rematch():
    f = open('sort_count_dic.txt','r')
    all_lines = f.readlines()
    f.close()
    standard_value = []
    for i in range(256):
        line = all_lines[i]
        line = line[line.find('[') + 1:line.find(']')]
        r,g,b = line.split(', ')
        standard_value.append([int(r),int(g),int(b)])
    need_match_value = {}
    count = 0
    for i in range(256, len(all_lines)):
        line = all_lines[i]
        line = line[line.find('[') + 1:line.find(']')]
        r,g,b = line.split(', ')
        key = str([int(r),int(g),int(b)])
        diff_list = [abs(j[0] - int(r)) + abs(j[1] - int(g)) + abs(j[2] - int(b)) for j in standard_value]
        min_diff_index = diff_list.index(min(diff_list))
        need_match_value[key] = standard_value[min_diff_index]
        count += 1
        print(get_runtime() + 'matching:{:.2f}%'.format(count*100/(len(all_lines) - 256)),end='\r')
    print('\n',end='')
    f = open('need_match_value.txt','w')
    for key, value in need_match_value.items():
        f.write(str(key) + ':' + str(value) + '\n')
    f.close()    

def rematch():
    xyz = np.load('int_xyz.npy')

    match_colors = np.load('int_colors.npy')
    match_colors = np.array(match_colors * 25.5, dtype=np.uint8)
    match_colors *= 10
    # print(match_colors)
    f = open('need_match_value.txt','r')
    all_lines = f.readlines()
    f.close()
    dic = {}
    for i in all_lines:
        key, value = i.split(':')
        dic[key] = [int(j) for j in value[1:-2].split(', ')]
    index = 0
    for i in match_colors:
        if str(i) in dic:
            value = dic[str(i)]
            match_colors[index][0], match_colors[index][1], match_colors[index][2] = value[0], value[1], value[2]
        index += 1
        print(get_runtime() + 'matching:{:.2f}'.format(index*100/len(match_colors)),end='\r')
    print('\n',end='')
    match_colors = match_colors / 255
    np.save('match_value.npy',match_colors)

def show_rebuild_with_rematch():
    xyz = np.load('data/npy/int_xyz.npy')
    match_colors = np.load('data/npy/match_value.npy')
    sztu_pcd = o3d.geometry.PointCloud()
    sztu_pcd.points = o3d.utility.Vector3dVector(xyz)
    sztu_pcd.colors = o3d.utility.Vector3dVector(match_colors)
    o3d.visualization.draw([sztu_pcd])

def rebuild_texture():
    f = open('sort_count_dic.txt','r')
    all_lines = f.readlines()
    f.close()
    colors_list = []
    for line in all_lines[:256]:
        line = line[line.find('[')+1:line.find(']')]
        r,g,b = line.split(', ')
        colors_list.append([int(b),int(g),int(r)])
    colors = np.array(colors_list, dtype=np.uint8)
    for i in range(len(colors)):
        img = np.reshape(colors[i], (1,1,3))
        cv2.imwrite('./rematch_texture/'+ str(i) + '.png', img)
        # color = np.array([])
if __name__ == '__main__':
    # opencv 默认为BGR ，open3d 默认为RGB
    # rebuild_texture()
    # img = np.array([255,0,0],dtype=np.uint8)
    # img = np.reshape(img,(1,1,3))
    # img = cv2.resize(img,(256,256))
    
    # match_colors, xyz = match_color()
    # match_colors_copy = match_colors_copy_read()
    # print(colors_255)
    # xyz_dis()
    # sztu_pcd.colors = o3d.utility.Vector3dVector(colors)
    # print(get_runtime()+'loading Vision')
    show_rebuild_with_rematch()
    # count_ahead256()
    # match_count_colors()

    # turn_count_256()
    # to_10_dic_count()

    # print('len(xyz):',len(xyz),'len(match_colors):',len(match_colors))
    # print(match_colors.shape)
    # match_colors = np.array(match_colors * 255, dtype=np.uint8)
    # match_colors = np.reshape(match_colors, (-1,1,3))
    # match_colors_copy = match_colors.copy()
    # match_colors_copy = cv2.cvtColor(match_colors_copy, cv2.COLOR_BGR2HSV)
    # match_colors_copy[:,:,1] = 70 #match_colors_copy[:,:1] * 1.05
    # match_colors_copy = cv2.cvtColor(match_colors_copy, cv2.COLOR_HSV2BGR)
    # match_colors_copy = np.array(match_colors_copy, dtype= np.uint8)
    # match_colors_copy = np.reshape(match_colors_copy, (-1,3))
    # match_colors_copy = match_colors_copy/255
    # np.save("match_colors_copy.npy", match_colors_copy)
    # print(match_colors_copy)
    # cv2.namedWindow('img',cv2.WINDOW_NORMAL)
    # cv2.imshow('img',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # img = match_colors
    # cv2.cvtColor(img, cv2.BGR)
    # show_source()
