import os
import cv2
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
        self.range_colors = []
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
            self.range_colors = range_colors_func()
        with Pool(processes=None) as p:
            p.map(counter, [0])
        self.data_area.sort_counter = np.array(self.data_area.sort_counter)
        counter()
        self.logger.info('finished counting')

    #生成材质包
    def spawn_texture(self):
        pwd = 'resources_pack/assets/colors_mod/textures/block'
        texture_list = []
        for num_list in self.range_colors:
            texture_list.append(num_list)
        for rgb, index in tqdm(zip(texture_list, range(256))):
            texture = np.array(rgb, dtype=np.uint8)
            texture = np.reshape(texture, (1,1,3))
            texture = cv2.cvtColor(texture, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'{pwd}/block_{index}.png', texture)

    #生成数据包
    def spawn_datapack(self):
        if os.path.exists('setblock'):
            self.logger.error(u"生成数据包失败，请检测当下目录是否包含上次生成的数据包，\
请删除或移走原有数据包，再执行程序")
        else:
            os.mkdir('setblock')
            os.mkdir('setblock/data')
            os.mkdir('setblock/data/setblock')
            os.mkdir('setblock/data/setblock/functions')
            with open('setblock/pack.mcmeta','w') as mcmeta:
                mcmeta.write(
'''{
    "pack": {
        "pack_format": 10,
        "description": "The test for setblock"
    }
}''')
            all_line:list[str] = []
            count = 0
            for xyz, rgb in tqdm(zip(self.data_area.unique_xyz, self.data_area.rematch_colors)):
                x, y, z = xyz
                index = self.range_colors.index(rgb)
                all_line.append(f'setblock {-x} {z+150} {y} colors_mod:block_{index}\n')
                if len(all_line) == 65536:
                    count += 1
                    self.logger.info(f'write {count} mcfunction')
                    with open(f'setblock/data/setblock/functions/setblock_{count}.mcfunction','w') as mcfunction:
                        mcfunction.writelines(all_line)
                    all_line = []
            if len(all_line) != 0:
                count += 1
                self.logger.info(f'write the last mcfunction')
                with open(f'setblock/data/setblock/functions/setblock_{count}.mcfunction','w') as mcfunction:
                    mcfunction.writelines(all_line)

def range_colors_func():
    range_colors = []
    sort_counter = np.load('data/sort_counter.npy')
    for key, _ in sort_counter[:256]:
        num_list = []
        for i in range(len(key)):
            if (key[i] == ' ' or key[i] == '[') and key[i+1].isnumeric():
                end = (i+1 + key[i + 1:].find(' ')) if key[i + 1:].find(' ') != -1 else len(key) - 1
                num_list.append(int(key[i+1:end]))
        range_colors.append(num_list)
    return range_colors

#用于多线程协同工作的回调函数
def match_colors(works):
    rematch_colors = []
    range_colors = range_colors_func()
    works_len = len(works)
    count = 0
    for index, rgb in works:
        diff_dict = {}
        for num_list in range_colors:
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

    if os.path.exists('data/unique_xyz.npy') and os.path.exists('data/unique_colors.npy'):
        logger.info('exist data, loading data')
        data_area.unique_colors = np.load('data/unique_colors.npy').tolist()
        data_area.unique_xyz = np.load('data/unique_xyz.npy').tolist()
    else:
        data_area.LoadingPCD()
        data_area.SaveIntNpy()

    process = Process(logger, data_area)
    if os.path.exists('data/sort_counter.npy'):
        logger.info('exist sort data')
        data_area.sort_counter = np.load('data/sort_counter.npy').tolist()
    else:
        process.Count_colors()

    if os.path.exists('data/rematch_colors.npy'):
        logger.info('exist sort rematch data')
        rematch_colors = np.load('data/rematch_colors.npy').tolist()
    else:
        logger.warning(f"matching colors data length: {len(data_area.unique_colors)} it took time")
        all_works = []
        cpu_num = cpu_count()
        for i in range(len(data_area.unique_colors)):
            if i < cpu_num:
                all_works.append([[i, data_area.unique_colors[i]]])
            else:
                all_works[i % cpu_num].append([i, data_area.unique_colors[i]])
        rematch_colors = []
        with Pool(processes=None) as p:
            for result in p.map(match_colors,iterable = all_works):
                rematch_colors += result
        np.save('data/rematch_colors.npy', np.array(rematch_colors))
        logger.info('finish save rematch_colors')
    rematch_colors = sorted(rematch_colors, key=lambda d:d[0][0])
    _, rematch_colors = list(zip(*rematch_colors))
    data_area.rematch_colors = rematch_colors

    if os.path.exists('resources_pack'):
        logger.info('have finished texture build')
    else:
        process.spawn_texture()
    process.spawn_datapack()
    logger.info("finish all work！")


