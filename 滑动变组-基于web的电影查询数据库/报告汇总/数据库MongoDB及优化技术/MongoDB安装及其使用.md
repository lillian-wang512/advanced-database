# 虚拟机安装MongoDB及其使用
## 本篇报告知识点
- MongoDB安装实操
- 数据库创建的基本操作（创建数据库、集合）
- 增删查改
- 用户管理
- 数据导入导出
- 主从复制（读写分离）
- 复制集（功能演示在课堂汇报完成）
  
  - 只有一个主节点（接受写操作，记录到oplog中），然后复制到从节点
  - 读请求默认指向主节点

## 实验环境

- 虚拟机：ubuntu20.04 
- mongoDB 4.4
- python3.9

## 实操过程

### 安装

- 安装之前建议更新Linux源

```bash
# 1、备份源文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak  
# 2、添加源到sources.list中
sudo gedit /etc/apt/sources.list

# 在打开的文本中，添加阿里源
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

# 3、更新源
sudo apt-get update

```

- 安装及配置文件
```bash
# 安装依赖包
sudo apt-get install libcurl4 openssl
# 关闭和卸载原有的mongodb
service mongodb stop
sudo apt-get remove mongodb

# 导入包管理系统使用的公钥
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
# 如果命令执行结果没有显示OK，则执行此命令在把上一句重新执行：sudo apt-get install gnupg

# 注册mongodb源
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# 更新源
sudo apt-get update

# 安装mongodb
sudo apt-get install -y mongodb-org=4.4.2 mongodb-org-server=4.4.2 mongodb-org-shell=4.4.2 mongodb-org-mongos=4.4.2 mongodb-org-tools=4.4.2
# 安装过程中如果提示: mongodb-org-tools : 依赖: mongodb-database-tools 但是它将不会被安装
# 终端下运行以下命令,解决:
# sudo apt-get autoremove mongodb-org-mongos mongodb-org-tools mongodb-org
# sudo apt-get install -y mongodb-org=4.4.2

# 创建数据存储目录
sudo mkdir -p /data/db

# 修改配置，开放27017端口
sudo vim /etc/mongod.conf
# 把12行附近的port=27017左边的#号去掉
```

### MongoDB 使用

- 启动和关闭MongoDB
```
# 重新加载配置，并启动mongodb
sudo systemctl daemon-reload
sudo systemctl start mongod

# 查看运行状态
sudo systemctl status mongod
# 如果mongodb状态为stop，则运行 sudo systemctl enable mongod

# 停止mongodb
sudo systemctl stop mongod

# 重启mongodb
sudo systemctl restart mongod
```

- 进入交互端
```
# 进入交互终端
mongo
```
     效果：
     MongoDB shell version v4.4.2
     connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
     Implicit session: session { "id" : UUID("2c920d56-ddbb-4649-9191-a3bd4506a2d2") }
     MongoDB server version: 4.4.2
     ---
      The server generated these startup warnings when booting: 
		# 警告：强烈建议使用XFS文件系统，并使用WiredIger存储引擎。
	        # 解释：因为当前ubuntu使用的是ext4文件系统，mongodb官方建议使用XFS文件系统功能更能发挥mongodb的性能，忽略不管
     2022-11-23T16:23:34.416+08:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
        # 警告：当前mongodb没有为数据库启用访问控制。对数据和配置的读写访问是不受限制的。
        # 解释：后面会创建数据库用户采用密码登陆的。暂时不用管
        2022-11-23T16:23:35.046+08:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
       ---
       ---
        Enable MongoDB's free cloud-based monitoring service, which will then receive and display
        metrics about your deployment (disk utilization, CPU, operation statistics, etc).

        The monitoring data will be available on a MongoDB website with a unique URL accessible to you
        and anyone you share the URL with. MongoDB may use this information to make product
        improvements and to suggest MongoDB products and deployment options to you.

        To enable free monitoring, run the following command: db.enableFreeMonitoring()
        To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
        ---

### 用户管理
  - 创建用户
  mongo的用户是以数据库为单位来建立的，每个数据库有自己的管理员。

    管理员可以管理所有数据库，但是不能直接管理其他数据库，要先在admin数据库认证后才可以。

    管理员的权限设置包含了2块，分别是角色和权限，由roles属性进行设置。
    ```
     db.createUser(user, writeConcern)
    {
    user: "<用户名>",
    pwd: "<密码>",
	customData: { <any information> }, # 任意内容，主要是为了表示用户身份的相关介绍 
	roles: [ # 角色和权限分配
		{ role: "<role>", db: "<database>" } | "<role>",
		...
    ]
    }
    ```
  - 给Admin数据库创建账户管理员
  当前账号只能用于管理数据库账号，不能进行数据库操作。
    ```
    # 进入/切换数据库到admin中
    use admin
    # 创建账户管理员
    db.createUser({
	  user: "admin",
	  pwd: "123",
	  roles: [
		  {role: "userAdminAnyDatabase",db:"admin"}
	   ]
     })
     ```
  - 创建用户自己的数据库的角色
   帐号是跟着数据库绑定的，所以是什么数据库的用户，就必须在指定库里授权和验证！！！
    ```
    # 切换数据库，如果当前库不存在则自动创建
    use mofang
    # 创建管理员用户
    db.createUser({
    user: "mofang",
    pwd: "123",
    roles: [
        { role: "dbOwner", db: "mofang"}
     ]
    })
    ```
### 库管理
- 显示所有数据库列表
  ```
  show dbs
  ```
- 切换数据库，如果数据库不存在则创建数据库
  ```
  use  <database>
  ```
- 查看当前工作的数据库
  ```
  db
  db.getName()
  ```
- 删除当前数据库，如果数据库不存在，也会返回{"ok":1}
  ```
  db.dropDatabase()
  ```

- 查看当前数据库状态
  ```
  > db.stats()

  {
	"db" : "mofang",
	"collections" : 0,
	"views" : 0,
	"objects" : 0,
	"avgObjSize" : 0,
	"dataSize" : 0,
	"storageSize" : 0,
	"totalSize" : 0,
	"indexes" : 0,
	"indexSize" : 0,
	"scaleFactor" : 1,
	"fileSize" : 0,
	"fsUsedSize" : 0,
	"fsTotalSize" : 0,
	"ok" : 1
   }
   ```
### 增删查改

```bash
# 插入
db.inventory.insertMany([
   // MongoDB adds the _id field with an ObjectId if _id is not present
   { item: "journal", qty: 25, status: "A",
       size: { h: 14, w: 21, uom: "cm" }, tags: [ "blank", "red" ] },
   { item: "notebook", qty: 50, status: "A",
       size: { h: 8.5, w: 11, uom: "in" }, tags: [ "red", "blank" ] },
   { item: "paper", qty: 100, status: "D",
       size: { h: 8.5, w: 11, uom: "in" }, tags: [ "red", "blank", "plain" ] },
   { item: "planner", qty: 75, status: "D",
       size: { h: 22.85, w: 30, uom: "cm" }, tags: [ "blank", "red" ] },
   { item: "postcard", qty: 45, status: "A",
       size: { h: 10, w: 15.25, uom: "cm" }, tags: [ "blue" ] }
]);
db.collection.insertOne() 

# 查询
db.inventory.find( { status: "D" } )
db.inventory.find( { size: { h: 14, w: 21, uom: "cm" } } )
db.inventory.find( { "size.uom": "in" } )
db.inventory.find( { tags: "red" } )
```

### 数据库连接

  后台mongod启动后使用mongo shell进行连接,连接遵循以下url格式

  > #### Connection String:
  >
  > `mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]`
  >
  > - **mongodb://** 这是固定的格式，必须要指定。
  > - **username:password@** 可选项，如果设置，在连接数据库服务器之后，驱动都会尝试登陆这个数据库
  > - **host1** 必须的指定至少一个host, host1 是这个URI唯一要填写的。它指定了要连接服务器的地址。如果要连接复制集，请指定多个主机地址。
  > - **portX** 可选的指定端口，如果不填，默认为27017
  > - **/database** 如果指定username:password@，连接并验证登陆指定数据库。若不指定，默认打开admin数据库。
  > - **?options** 是连接选项。如果不使用/database，则前面需要加上/。所有连接选项都是键值对name=value，键值对之间通过&或;（分号）隔开

- 方法1 MongoDB shell
实例如下：
  ```bash
  # 此时连接本地默认端口27017
  mongo 
  # 指定端口
  mongo --port 28015
  # 连接远程端口
  mongo "mongodb://mongodb0.example.com:27017"
  # 带认证的连接
  mongo "mongodb://alice@mongodb0.examples.com:27017/?authSource=admin"
  # 开启TLS/SSL 
  mongo "mongodb://mongodb0.example.com.local:27017,mongodb1.example.com.local:27017,mongodb2.example.com.local:27017/?replicaSet=replA&ssl=true"
  ```

- 方法2 通过其他编程接口


### python远程操作

```bash
# 安装pymongo模块 
pip install pymongo -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

# 配置mongoDB允许远程连接
sudo vim  /etc/mongod.conf
bind_ip 设置为0.0.0.0
systemctl restart mongod 
sudo ufw allow 27017
```

### 主从复制（读写分离）及复制集
  - 只有一个主节点（接受写操作，记录到oplog中），然后复制到从节点
  - 读请求默认指向主节点
```bash
# 配置文件
sudo vim /etc/mongod.conf

replication:
  replSetName:
sudo systemctl enable mongod
sudo systemctl restart  mongod

# 连接mongod
sudo mongo

# 查看复制集状态
rs.status()

# 在任一节点上执行复制集初始化命令
rs.initiate( {
  _id : "rs0",
  members: [
      { _id: 0, host: "192.168.56.102:27017" },
      { _id: 1, host: "192.168.56.104:27017" },
      { _id: 2, host: "192.168.56.105:27017" }
  ]
})

# 删除数据库
db.dropDatabase();

# 测试数据同步功能
# 主节点
use test
db.test.insertOne({"name": "kenny"})

# 从节点查询
use test
rs.slaveOk()
db.test.find()

# 测试主节点选举功能
# 强制关闭主节点上的MongoDB服务，然后重新登入mongo shell
use admin
db.shutdownServer()
rs.isMaster()

# 查看端口
ps -ef | grep mongo
netstate  -tlnp

# 修改主机标识
cat /etc/machine-id
```

## 参考资料

[install-mongodb-on-ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)