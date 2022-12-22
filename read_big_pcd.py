# f = open('3D-models/terra_pcd/cloudAB.pcd','r', encoding='gbk')
# a = f.readline()
# print(len(a))
# f.close()
import open3d as O3d
import numpy as np
def o3dpcd():
    complex_pcd_path = '3D-models/terra_pcd/cloudAB.pcd'
    o3d = O3d
    pcd = o3d.io.read_point_cloud(complex_pcd_path)
    # size = (np.asarray(pcd.points)).size
    # length = pow(size,1/3)
    # print(length)
    # print((np.asarray(pcd.points)).shape)
    # x, y, z = zip(*np.asarray(pcd.points))
    # print('x:',max(x)-min(x))
    # print('y:',max(y)-min(y))
    # print('z:',max(z)-min(z))
    # print((np.asarray(pcd.colors)*255).size)
    # print(dir(pcd))
    points = np.asarray(pcd.points)
    np.save('cloudABxyz.npy',points)
    # f = open('cloudABxyz.txt','w')
    # for x, y, z in points:
    #     wri_str = '{:.2f}'.format(x) + ' ' + '{:.2f}'.format(y) + ' ' + '{:.2f}'.format(z) + '\n'
    #     f.write(wri_str)
    # f.close()

    # np.save('cloudABrgb.npy', np.asarray(pcd.colors))
    # colors = np.asarray(pcd.colors)*255
    # f = open('cloudABrgb.txt','w')
    # for r, g, b in colors:
    #     col_str = str(int(r)) + ' ' + str(int(g)) + ' ' + str(int(b)) + '\n'
    #     f.write(col_str)
    # f.close()
    # o3d.visualization.draw_geometries([pcd], window_name="Open3D",width=1280,height=720)
o3dpcd()