# 使用Docker快速搭建Mongodb

## 实验环境

- 虚拟机：ubuntu20.04 
- mongoDB 4.0
- python3.6
- windows10

## 操作过程

### Docker安装

- 在虚拟机：ubuntu20.04 中安装docker

  ```bash
  # 更新源
  $ sudo apt-get update
  # 安装docker
  $ sudo apt-get install docker.io
  # 启动docker服务
  $ sudo systemctl start docker
  # 查看docker状态
  $ sudo systemctl status docker
  # 停止docker服务
  $ sudo systemctl stop docker
  # 查看docker版本
  $ sudo docker version
  ```

### Docker安装相关问题排错

  - 重启后Docker远程无法连接

    1. 修改文件:

       `vim /usr/lib/sysctl.d/50-default.conf`

        在最后一行追加：`net.ipv4.ip_forward = 1`

      2. 重启运行虚拟机 或者执行`sysctl -p`

    3. `sysctl net.ipv4.ip_forward` 查看结果是否为1

    4. 启动镜像

    - docker: Error response from daemon: Conflict. The container name “XXX” is already in use by container “XXX”. You have to remove (or rename) that container to be able to reuse that name.

  - docker name重名，改名容器或者删除重建容器

  -  docker is running but cannot access  or stop 

     - 遭遇相关进程问题，利用docker ps语句查看相关进程，必要时kill掉多余或故障进程。

### Docker安装成功后，进行Mongodb的配置

  ```bash
  # 拉取Mongodb镜像
  $ sudo docker pull mongo
  # 查看是否有Mongo镜像
  $ sudo docker image
  # 创建文件夹，以便后续将容器内文件映射到虚拟机内
  $ sudo mkdir /mysoft && cd /mysoft
  $ sudo mkdir mongodb && cd mongodb
  $ sudo mkdir configdb && sudo mkdir db
  # 创建容器，开放27017、28017两个端口，将容器内/data/configdb/和/data/db/映射到虚拟机内
  $ sudo docker run -d -p 27017:27017 -p 28017:28017 -v /mysoft/mongodb/configdb:/data/configdb/ -v /mysoft/mongodb/db/:/data/db/ --name mongodb mongo
  # 如果有需要，可进入容器内进行Mongodb的配置
  $ sudo docker exec -it  mongodb  mongo admin
  # 安装成功，查看容器的运行信息
  $ sudo docker ps
  ```

  ### mongoDB相关使用

  ```bash
  # 导入公钥
  sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
  # 添加apt源
  echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
  # apt-get 下载 
  sudo apt-get update
  sudo apt-get install -y mongodb-org
  # 关闭自动更新
  echo "mongodb-org hold" | sudo dpkg --set-selections
  echo "mongodb-org-server hold" | sudo dpkg --set-selections
  echo "mongodb-org-shell hold" | sudo dpkg --set-selections
  echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
  echo "mongodb-org-tools hold" | sudo dpkg --set-selections
  # 服务启动关闭
  sudo service mongod stop
  # 日志文件
  /var/log/mongodb/mongod.log
  ```

