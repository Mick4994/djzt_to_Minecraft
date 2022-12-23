import os
import logging
import open3d as o3d
import numpy as np
from tqdm import tqdm, trange
from utils.mylog import log_init


class Data_Area:
    def __init__(self, logger:logging.Logger) -> None:
        self.float_xyz:list[float] = []
        self.float_colors:list[float] = []
        self.int_xyz_dic = {}
        self.unque_xyz:list[int] = []
        self.unque_colors:list[list[int]] = []
        self.rematch_colors = []
        self.colors_counter = {}
        self.sort_counter = []
        self.logger = logger
    def LoadingPCD(self):
        self.logger.info('loading pcd')
        all_pcd_file = os.listdir('3D-models/terra_pcd/')
        all_pcd_file = ['3D-models/terra_pcd/' + i for i in all_pcd_file if i.endswith('.pcd')]
        pcd_list = [o3d.io.read_point_cloud(pcd_file) for pcd_file in all_pcd_file]
        self.logger.info('getting xyz and colors')
        for i, index in tqdm( list (zip(pcd_list, range(len(pcd_list))))):
            self.float_xyz += np.asarray(i.points).tolist()
            self.float_colors += np.asarray(i.colors).tolist()
            self.logger.info(f"get {index}")
        for xyz, rgb in tqdm( list (zip(self.float_xyz, self.float_colors))): # 传入字典去重
            self.int_xyz_dic[str([int(i) for i in xyz])] = [int(i*25.5)*10 for i in rgb]
    def SaveIntNpy(self):
        for key, value in tqdm(self.int_xyz_dic.items()):
            a,b,c = key[1:-1].split(',')
            self.unque_xyz.append([int(a),int(b),int(c)])
            self.unque_colors.append(value)
        np.save('unque_xyz.npy',np.array(self.unque_xyz))
        np.save('unque_colors.npy',np.array(self.unque_colors)) # 整型坐标下对应的颜色RGB
        self.logger.info('finish save numpy data')

class Process:
    def __init__(self, logger:logging.Logger, data_area:Data_Area) -> None:
        self.logger = logger
        self.data_area = data_area
    def Count_colors(self):
        for _, rgb in tqdm(self.data_area.int_xyz_dic.items()):
            try:
                self.data_area.colors_counter[str(rgb)] += 1
            except:
                self.data_area.colors_counter[str(rgb)] = 0
        self.data_area.sort_counter = sorted(self.data_area.colors_counter.items(), 
                                               key = lambda kv:(kv[1], kv[0]),
                                               reverse = True)
    def match_colors(self):
        for rgb in tqdm(self.data_area.unque_colors):
            diff_dict = {}
            for key, _ in zip(self.data_area.sort_counter[:256]):
                a,b,c = key[1:-1].split(',')
                rgb_match = [int(a), int(b), int(c)]
                diff = sum([abs(i-j) for i, j in zip(rgb, rgb_match)])
                diff_dict[diff] = rgb_match
            diff_list = sorted(diff_dict.items(), key = lambda d:d[0])
            min_rematch_rgb = diff_list[0][1]
            self.data_area.rematch_colors.append(min_rematch_rgb)

if __name__ == "__main__":
    logger = log_init()
    data_area = Data_Area(logger)
    process = Process(logger, data_area)

    data_area.LoadingPCD()
    data_area.SaveIntNpy()

    process.Count_colors()
    process.match_colors()

