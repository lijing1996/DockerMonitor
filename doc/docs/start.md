## 申请集群账号及权限
所有申请AI集群节点权限的学生需要[发邮件给王金磊老师](mailto:wangjinlei@shanghaitech.edu.cn)并抄送你的导师, 邮件内容包括:

1. 你的名字
2. 上科大邮箱
3. 资源需求情况
4. 需要多长时间
5. 原因

## 登录AI集群
请成功后, 你会收到类似如下信息:
```
username: piaozx
password: 123456
port: 22100
admin_open_port: 31000-31009
```
其中`username`为你的用户名(但是在登录时不会用到), `password`是你的初始登录密码, `port`是你登录用的端口号, `admin_open_port`是为开启网络服务预留的端口号(如`visdom`, `jupyter`)

接下来我们用ssh登录即可(注意, 登录时用户名为`root`):
```
ssh root@10.19.124.11 -p 22100
```
windows上的cmd默认没有ssh, 在这里推荐使用`WSL`(Windows Subsystem for Linux), 具体网上教程用很多, 不再赘述.
```bash
# piaozhx @ pzx-mbp in ~ [18:43:17]
$ ssh root@10.19.124.11 -p 22100
root@10.19.124.11's password:
Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 3.10.0-514.16.1.el7.x86_64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
  If you have any problem, go to AI server website
  ADMIN OPEN PORT: 31000-31009
 .............................................
Last login: Mon Aug 27 10:30:35 2018 from 10.20.194.83

# root @ piaozx.admin in ~ [12:01:43]
$
```
其中:

* `root`表示你目前的用户是root(这是因为集群目前使用docker的container作为资源和权限管理, 每个用户在自己的container中都是root, 你可以随意安装你想要的配置文件)
* `piaozx`是你申请的用户名
* `admin`表示你目前在admin节点中, 访问任何计算节点都必须要先登录admin节点



!!! warning "注意"
    登录之后, 你需要尽快修改你的默认密码
    
    ```
    $ passwd
    ```
    

## 登录计算节点

```
$ ssh node01
```
只需要通过`ssh`登录即可. 注意, 所有的ssh登录都是RSA公钥加密登录, 如果你不知道你在做什么, 请不要随便改动/root/.ssh文件夹内的文件.

