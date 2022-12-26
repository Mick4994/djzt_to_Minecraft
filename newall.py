import os
import cv2
import re
import logging
import open3d as o3d
import numpy as np
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from utils.mylog import log_init


class Data_Area:
    def __init__(self, logger:logging.Logger) -> None:
        self.float_xyz:list[float] = []
        self.float_colors:list[float] = []
        self.int_xyz_dic = {}
        self.unique_xyz:list[int] = []
        self.unique_colors:list[list[int]] = []
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
        self.logger.info("finished get, dict delete duplicate elements")
        for xyz, rgb in tqdm( list (zip(self.float_xyz, self.float_colors))): # 传入字典去重
            self.int_xyz_dic[str([int(i) for i in xyz])] = [int(i*25.5)*10 for i in rgb]
    def SaveIntNpy(self):
        for key, value in tqdm(self.int_xyz_dic.items()):
            a,b,c = key[1:-1].split(',')
            self.unique_xyz.append([int(a),int(b),int(c)])
            self.unique_colors.append(value)
        np.save('unique_xyz.npy',np.array(self.unique_xyz))
        np.save('unique_colors.npy',np.array(self.unique_colors)) # 整型坐标下对应的颜色RGB
        self.logger.info('finish save numpy data')

class Process:
    def __init__(self, logger:logging.Logger, data_area:Data_Area) -> None:
        self.logger = logger
        self.data_area = data_area
    def Count_colors(self):
        self.logger.info("Count all colors and down sort")
        def counter(not_arg = None):
            for rgb in tqdm(self.data_area.unique_colors):
                try:
                    self.data_area.colors_counter[str(rgb)] += 1
                except:
                    self.data_area.colors_counter[str(rgb)] = 0
            self.data_area.sort_counter = sorted(self.data_area.colors_counter.items(), 
                                                key = lambda kv:(kv[1], kv[0]),
                                                reverse = True)
            np.save("sort_counter.npy", np.array(self.data_area.sort_counter))
        with Pool(processes=None) as p:
            p.map(counter, [0])
        self.data_area.sort_counter = np.array(self.data_area.sort_counter)
        counter()
        self.logger.info('finished counting')

            # if count % pow(10, len(str(unique_colors_len)) - 2) == 0:
            #     self.logger.info(f"\nmatching {count}/{unique_colors_len}:{count*100/unique_colors_len:.2f}%")
    def spawn_texture(self):
        if not os.path.exists('new_texture'):
            os.mkdir('new_texture')
        for item, index in tqdm(zip(self.data_area.sort_counter[:256], range(256))):
            texture = np.array(item[0], dtype=np.uint8)
            texture = np.reshape(texture, (1,1,3))
            texture = cv2.cvtColor(texture, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'new_texture/block_{index}.png', texture)
    def spawn_datapack(self):
        if os.path.exists('setblock'):
            self.logger.error(u"生成数据包失败，请检测当下目录是否包含上次生成的数据包，\
                                请删除或移走原有数据包，再执行程序")
        else:
            os.mkdir('setblock')
            os.mkdir('setblock/data')
            os.mkdir('setblock/data/functions')
            with open('setblock/pack.mcmeta','w') as mcmeta:
                mcmeta.write(
'''{
    "pack": {
        "pack_format": 10,
        "description": "The test for setblock"
    }
}''')
            all_line:list[str] = []
            for xyz, rgb in tqdm(zip(self.data_area.unique_xyz, self.data_area.rematch_colors)):
                x, y, z = str(xyz)[1:-1].split(',')
                index = self.data_area.rematch_colors.index(rgb)
                all_line.append(f'setblock {x} {y} {z} colors_mod:block_{index}\n')
            with open('setblock/data/functions/setblock.mcfunction','w') as mcfunction:
                mcfunction.writelines(all_line)

sort_counter = np.load('sort_counter.npy')

def match_colors(works):
    rematch_colors = []
    works_len = len(works)
    count = 0
    for index, rgb in works:
        diff_dict = {}
        for key, _ in sort_counter[:256]:
            num_list = []
            for i in range(len(key)):
                if (key[i] == ' ' or key[i] == '[') and key[i+1].isnumeric():
                    end = (i+1 + key[i + 1:].find(' ')) if key[i + 1:].find(' ') != -1 else len(key) - 1
                    num_list.append(key[i+1:end])
            a, b, c = num_list
            rgb_match = [int(a), int(b), int(c)]
            diff = sum([abs(i-j) for i, j in zip(rgb, rgb_match)])
            diff_dict[diff] = rgb_match
        diff_list = sorted(diff_dict.items(), key = lambda d:d[0])
        min_rematch_rgb = diff_list[0][1]
        rematch_colors.append([[index, 0, 0], min_rematch_rgb])
        count += 1
        if count % pow(10, len(str(works_len)) - 2) == 0:
            print(f'cpu index {works[0][0]}: matching {count*100/works_len:.2f}%')
    return rematch_colors

if __name__ == "__main__":
    logger = log_init()
    data_area = Data_Area(logger)

    if os.path.exists('unique_xyz.npy') and os.path.exists('unique_colors.npy'):
        logger.info('exist data, loading data')
        data_area.unique_colors = np.load('unique_colors.npy').tolist()
        data_area.unique_xyz = np.load('unique_xyz.npy').tolist()
    else:
        data_area.LoadingPCD()
        data_area.SaveIntNpy()

    process = Process(logger, data_area)
    if os.path.exists('sort_counter.npy'):
        logger.info('exist sort data')
        data_area.sort_counter = np.load('sort_counter.npy').tolist()
    else:
        process.Count_colors()

    if os.path.exists('rematch_colors.npy'):
        logger.info('exist sort rematch data')
        rematch_colors = np.load('rematch_colors.npy')
        print(rematch_colors.shape)
    else:
        logger.warning(f"matching colors data length: {len(data_area.unique_colors)} it took time")
        all_works = []
        for i in range(len(data_area.unique_colors)):
            if i < 12:
                all_works.append([[i, data_area.unique_colors[i]]])
            else:
                all_works[i%12].append([i, data_area.unique_colors[i]])
        rematch_colors = []
        with Pool(processes=None) as p:
            for result in p.map(match_colors,iterable = all_works):
                rematch_colors += result
        np.save('rematch_colors.npy', np.array(rematch_colors))
        logger.info('finish save rematch_colors')

    # logger.info('finished rematching')
    # process.spawn_texture()
    # process.spawn_datapack()
    # print(cpu_count())

