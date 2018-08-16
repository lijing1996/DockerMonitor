# Getting Started
### Request for Computing Resource in AI Cluster
All students should send an requst email to Wang Jinlei and CC your advisor. Requests MUST contain the following:

Your Name
Your Shanghaitech Email Address
Resource You Need (CPU/GPU)
Number of CPU/GPU Cores You Need
Storage Space You Need
How Long You Need to Use (At Most 2 Weeks in Principle)
For What Purpose You Apply for Above Resources
Access AI Cluster
After your request is comfirmed, you’ll receive a letter containing username and initial password you need to login AI cluster. To access AI cluster, just type the following command in your favorate terminal:

ssh username@10.19.124.11
For Windows users, MobaXterm is the recommanded terminal.

You will be asked for your password to continue.

```
Fri Jun 30 13:22:13 2017
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 375.26                 Driver Version: 375.26                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 1080    Off  | 0000:02:00.0     Off |                  N/A |
| 27%   31C    P0    38W / 180W |      0MiB /  8113MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   1  GeForce GTX 1080    Off  | 0000:03:00.0     Off |                  N/A |
| 27%   34C    P0    38W / 180W |      0MiB /  8113MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   2  GeForce GTX 1080    Off  | 0000:83:00.0     Off |                  N/A |
| 27%   28C    P0    38W / 180W |      0MiB /  8113MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   3  GeForce GTX 1080    Off  | 0000:84:00.0     Off |                  N/A |
|  0%   29C    P0    34W / 180W |      0MiB /  8113MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID  Type  Process name                               Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

How To Make Command Running in the Background
If you directly run come commands in your terminal, their processes will be termimated once you disconnect from AI cluster. In order to make your command stay alive after you close the terminal session, you have to make your command process run in background using nohup command args &. Optionally, you can specify the file where the stdout will be redirected. Here are some examples:

# run a training scripts in the background and redirect stdout to file "out.txt"
nohup python train.py --lr 0.1 --epochs 100 >> out.txt &
Then you can use tailf out.txt to monitor your script’s output. You can safely use CTRL-C to terminate tailf command without effect on your script. If you want to terminate your command running in the background, you should first get the process id(PID) of your command. This can be done using ps aux, you will see a list of process running on the node. You can use grep to filter the output, like the following:

# find the PID of processes whose name containing key words "python"
ps aux | grep python
You will only see all process whose command line contain key words python. Then, you can get your process PID in the corresponding column of the output. To terminate your command process, enter the following command:

kill -9 12345 23456
where 12345 and 23456 are PIDs of the processes you wish to terminate.

Working With AI Cluster The Best Practice
Access to Internet or Other Nodes
Users should note that only admin node have internet access. Therefore if you want to download something from internet, you should download it on admin node. All nodes in the cluster share the same filesystem, which means that once you download something on admin node, you have it on all other nodes. There two kinds of networks in AI cluster: job network and IB network. The former is used in most cases (e.g. ssh login) while the later provides high speed communications between nodes. Hostnames nodeXX are resolved to the job network ip 10.10.10.1XX and inodeXX are resolved to the IB network ip 12.12.12.1XX. Users who need high speed communication between nodes are recommanded to use IB network.

Note
Because shared storage uses IB network, heavy usage of IB network may slow down I/O speed.

Request For Sudo Privilege
All users should not request for sudo privilege in most situations. Users accustomed to work with their personal computers may like to use sudo apt-get install blablabla to install all softwares and liberaries, however, it is not necessary to use root privilege if you just install them in your own directories. All commonly used liberaries and softwares have already been installed in the system, all users who need extra softwares or libraries should firstly try to install them in their own directory and use environment variables like PATH and LD_LIBRARY_PATH to declare the new software executable file or libraries.

The Best Practice For Python Users
We highly recommend python users to setup their own anaconda environment. Their are plenty of advantages using anaconda:

Easy to install new packages using conda or pip command, without requiring admin privilege.
Making users’ python environment seperated from system python environment.
Some python packages just provide wrappers for some C++ libraries, hence needs underlying C++ liberaries to be installed. Anaconda will handle all these dependencies elegantly.
If their are some reasons you really need system python environment and want to install some packages. You SHOULD install it into your home directory with the following command.

pip install package-name --user
How to Run Applications With GUI
Some users may need to use softwares with GUI (e.g. matlab, pycharm), which is possible using ssh X11 forwarding. AI cluster is configured to support X11 forwarding, but users need to add extra lines into their .bashrc file to make X11 forwarding run properly. In order to enable X11 forwarding feature, add the following lines into .bashrc:

export XAUTHORITY=/home/$(whoami)/.Xauthority
if [ -f "./DISPLAY" ]
then
        export DISPLAY=$(cat ./DISPLAY)
        xauth add $(cat ./DISPLAYSESSION)
fi
Then user should re-login AI cluster with

ssh -X username@10.19.124.11
where the option -X enables X11 forwarding feature. Now you can feel free to run graphics applications, for example, you can try to run matlab and you will see matlab main window on your local PC. The ssh X11 forwarding can be chained, for example, it’s possible to run GUI applications on nodes other than admin node.

# on your local PC
ssh -X username@10.19.124.11
# on admin node
ssh -X node01
# then you can run GUI applications like matlab on node01
matlab