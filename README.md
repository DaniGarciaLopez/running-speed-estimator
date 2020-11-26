# Estimate the running speed of a human from a video stream
## Installation
> The following steps were perform to sucessfully install OpenPose 1.7 in a fresh Ubuntu 18.04 system. In order to install it in a different environment you may need another configuration. Please refer to the [official installation instructions](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/README.md) to proceed.
### Prerequisites
#### Install Cuda 10.0 and CuDNN 7
Purge existing CUDA first
```
sudo apt --purge remove "cublas*" "cuda*"
sudo apt --purge remove "nvidia*"
```
Install CUDA Toolkit 10
```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub && sudo apt update
sudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb

sudo apt update
sudo apt install -y cuda=10.0.130-1
```
Install CuDNN 7 and NCCL 2
```
wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo dpkg -i nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb

sudo apt update
sudo apt install -y libcudnn7 libcudnn7-dev libnccl2 libc-ares-dev

sudo apt autoremove
```
```
echo 'export PATH=/usr/local/cuda-10.0/bin${PATH:+:${PATH}}' >> ~/.bashrc
```
Reboot computer
```
reboot
```
Type `nvidia-smi` and `nvcc --version` to verify your installation.

#### Install Nvidia drivers - Nvidia 1080 (**Only if screen has problems after reboot**)
```
sudo apt install nvidia-driver-430
```
Reboot computer
```
reboot
```
#### Clone repository
```
cd
git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
```
#### Uninstall Anaconda (if any)
> Anaconda includes a Protobuf version that is incompatible with Caffe. Either you uninstall anaconda and install protobuf via apt-get, or you compile your own Caffe and link it to OpenPose.
```
rm -rf anaconda3/
```
Note: simple remove is good enough, although purge can work fine too.
#### Install protobu
```
sudo apt-get install autoconf automake libtool curl make g++ unzip -y
git clone https://github.com/google/protobuf.git
cd protobuf
git submodule update --init --recursive
./autogen.sh
./configure
make
make check
sudo make install
sudo ldconfig
```
#### Install CMake GUI
> Important: CMake 3.16 has issues with OpenSSL, use 3.15 instead. Required CMake version > = 3.12.
```
sudo apt purge cmake-qt-gui
sudo apt-get install qtbase5-dev
```
Download CMake from the website, move it to home, unzip it and go inside that folder. In my case, I picked [cmake-3.15.6.tar.gz](https://github.com/Kitware/CMake/releases/download/v3.15.6/cmake-3.15.6.tar.gz).
```
./configure --qt-gui
./bootstrap && make -j`nproc` && sudo make install -j`nproc`
```
#### Install Caffe
```
cd openpose
sudo bash ./scripts/ubuntu/install_deps.sh  ## Prerequisites
sudo apt install caffe-cuda
```
#### Install OpenCV
```
sudo apt-get install libopencv-dev
$ pkg-config --modversion opencv   ## current latest version is 3.2
```
Run the following command if and only if there is "cv2" not found error when running python example:
```
pip3 install opencv-python==3.2.0.8

```
### Build OpenPose
```
cd openpose/3rdparty
git clone https://github.com/CMU-Perceptual-Computing-Lab/caffe.git
```
Create an empty subcategory “build” folder inside Openpose folder:
```
cd openpose
mkdir build
```
1) Open CMake GUI you just installed.
```
cmake-gui
```
2) Select Openpose source code directory path and build directory path.
3) Select Configure to compile the files. A dialog box appears CMakeSetup. Select "Unix Makefiles" and "Use default native compilers". Click finish.
4) It takes some time to download models and compiling it. If any error happens it may be of CUDA or cuDNN installation. After successful configuration, check the “BUILD_PYTHON” inside the red box.
![image](https://github.com/DaniGarciaLopez/running-speed-estimator/blob/main/cmake.png?raw=true)
5) Click "Generate". It will show "Generating done" if no errors.
6) Close the CMake and proceed with these commands in your terminal to build OpenPose:
```
cd openpose/build/
make -j`nproc`
```
Compile OpenPose source:
```
cd openpose/build/
sudo make install
```
Compile and build python OpenPose:
```
cd openpose/build/python/openpose
sudo make install
```
### Test OpenPose
```
cd openpose
./build/examples/openpose/openpose.bin --video examples/media/video.avi
```
Test Python API
```
cd openpose/build/examples/tutorial_api_python
python3 openpose_python.py
```
![image](https://github.com/tramper2/openpose/blob/master/doc/media/shake.gif)
### References
- [OpenPose Installation](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/README.md)
- [A 2020 Guide for Installing OpenPose](https://medium.com/@erica.z.zheng/installing-openpose-on-ubuntu-18-04-cuda-10-ebb371cf3442)
- [Python OpenPose Installation](https://robinreni96.github.io/computervision/Python-Openpose-Installation/)
- [Install CUDA 10 on Ubuntu 18.04](https://gist.github.com/bogdan-kulynych/f64eb148eeef9696c70d485a76e42c3a)
