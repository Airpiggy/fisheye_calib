# 鱼眼摄像头标定+矫正
## 依赖
如果使用`conda`，则：
```bash
conda install opencv-contrib-python numpy matplotlib
```
普通`pip`：
```bash
pip install opencv-contrib-python numpy matplotlib
```
## 使用方法
> 本项目中主要有两个文件：`fisheye_calib.py`和`calib_result_preview.py`，前者用于标定相机内参和畸变参数的标定，后者用于展示当前标定结果对视频流的矫正效果。
### 标定-`fisheye_calib.py`
标定前需要提前打印好目录中的棋牌格pdf文件。
使用的话进入到该项目的目录后，运行下面的指令：
```bash
python fisheye_calib.py [index_of_your_camera]
```
如果你的设备上只有一个摄像头，那么索引一般为0（Mac设备除外），我是在树莓派平台上，且只有一个摄像头因此我的指令是：
```bash
python fisheye_calib.py 0
```
具体检查摄像头的索引可以通过：
```bash
sudo apt update
sudo apt install v4l2-utils
v4l2-ctl --list-devices
```
程序运行成功后会显示一个灰度图像和一个彩色图像，程序会在彩色图像中显示对棋盘格的检测。将摄像头对准棋盘格并不断改变角度，同时按下键盘上的`s`键并存储后续标定所用的数据（为了标定的效果，我将这个数据数量的最小值设置为50份），每按下一次终端中会显示目前数据是否足够以及最少还需要多少份数据。
数据收集完后按`q`键，程序开始标定参数，并将标定结果输出在终端并存储为`fisheye_calibration_result.npz`，这个文件后续会被`calib_result_preview.py`使用到。
### 结果预览
在终端中运行：
```bash
python calib_result_preview.py 0
```
此时便会显示两个窗口，一个是原鱼眼视频流，一个是矫正后的效果。