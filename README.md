# EMS - Euler Method Simulation
### Prereq
```sh
$ sudo apt-get install python-numpy python-scipy python-matplotlib
$ sudo apt-get install ffmpeg
$ sudo apt-get install libboost-python1.58-dev
```

### Prepare MNIST
```sh
$ mkdir ~/Documents/MNIST_data
$ cd ~/Documents/MNIST_data/
$ wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
$ wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
$ wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
$ wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
$ gzip -d *.gz
```

### Download/Build
```sh
$ cd ~/Documents
$ git clone https://github.com/msmania/ems.git -b dev ems
$ cd ems/c/
$ make
```

### Run
```sh
$ cd ~/Documents/ems/
$ export DISPLAY=:0
$ python emstest.py basic
$ python emstest.py bulk
$ export N=20
$ python mnist.py 20.mp4
```
