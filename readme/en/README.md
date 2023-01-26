<h1>
  <p align="center">
    <img src="../resources/icon.png" alt="Logo" width="200" height="150">
    <br>
    DJZT_To_Minecraft
  </p>
</h1>

## Description

This is a 3D model(.pcd file) to minecraft function(.mcfunction file) program, 

## Installation

* Require [Windows>=10]() operating system, [Python>=3.6](https://www.python.org/) and [git](https://git-scm.com/) and [Minecraft 1.18.2]().
* Create a new folder and open the command line under it, and run `git clone https://github.com/Mick4994/djzt_to_Minecraft.git`.
* Run `pip install requirement.txt -r` in your command line to Install dependent libraries, Users in Chinese Mainland add `-i https://pypi.tuna.tsinghua.edu.cn/simple` after this command.
* Place pcd file in `/ 3D-models/terra_ Pcd/` directory.
* When the installation is completed, Run `python main-nogui.py`.

## Run

* Load pcd file: prompt `loading pcd`, which usually takes several tens of seconds. When prompt `finish save null data`
* Generate material package: generate `resource_pack` folder in the main directory, compresse into a`. zip `file, which is the Minecraft material package file.
* Convert model data: the waiting time for this step is long, please wait patiently, and the console will prompt the progress.
* Generate data package: generate the `setblock` folder under the main directory, and then manually put it into the directory where the Minecraft data package file is placed
* Wait for the console log to prompt `finish all work!`

Note: The data of the previous step will be cached before the start of each step. The cache file is in the format of `. npy`. Do not delete it until the operation is completed

## Development

#### Version planning

* V1 (currently completed) (no gui version and no packet):
1. Separate and objectify data area and program area.
2. Add console progress bar and log library records.
3. Multi-threaded processing of large amount of conversion work.

* V2 (future) (develop the gui version for more convenient use):
1. Develop gui and beautify the interface.
2. Compatible with more model files?
3. Compatible with more Minecraft versions?
4. Add small block mod to further improve the dimensional accuracy imported into Minecraft.
5. Redevelop Minecraft mod to expand color space.

#### Development preparation

requirements:
1. Have the ability to develop Python and Java programs
2. Have a certain understanding of the operation mechanism of Minecraft
3. Basic modeling software

Note：One of the above conditions is enough, more is better.

* After completing the installation, use the integrated development environment or editor, such as Pycharm, vscode, etc., to open the workspace `djzt_ to_ Minecraft`.
* The process of building the Minecraft Fabric development environment is complicated. For detailed tutorials, please watch: [Re: module programming from scratch - ep-1 boring to the extreme but once and for all environment building](https://www.bilibili.com/video/BV11a411a7uT/)
* You can open pcd or obj model file with modeling software, such as the `Windows 3D viewer` or `blender` (used to open obj files).
* If you want to contact the first author : Mick4994, QQ: `1140239446`




