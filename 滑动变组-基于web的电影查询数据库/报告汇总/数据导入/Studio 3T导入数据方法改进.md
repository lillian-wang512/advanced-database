# 使用 Studio 3T 远程连接 Mongodb
为了提高开发效率，Studio 3T支持远程连接数据库、数据可视化、SQL语句开发和一键导入数据等功能，所以我们选择此改进方法

## 实验环境

- MongoDB 4.4
- ubuntu 20.04
- windows10
- Studio 3T

## 实操过程

### 准备条件

- 安装好MongoDB并查看和确保MongoDB正常运行和27017端口已经开放
  ```
  sudo netstat -antlp
  ```
- 配置MongoDB允许远程连接
  ```
  sudo vim  /etc/mongod.conf
   bind_ip 设置为0.0.0.0
  systemctl restart mongod
  ``` 

### Studio 3T导入数据
- 下载Studio 3T完成后点击启动

- 点击左上角的 `Connect` 进行数据库连接

    ![](img/3T-CONNECT.png)
    
- 点击左上角新建连接

    ![](img/3T-NEWCONNECTION.png)
    
- 如下图所示，给该连接起名W为 `mongodb` ，3T默认连接的是本地的 27017 端口，但由于我们的数据库在虚拟机里，所以我们需要把原有的localhost修改为我们自己的虚拟机ip地址

    ![](img/3T-TEST.png)
    
 - 填写完后点击左下角的 `Test Connection` ，测试是否能正常连接
    
- 测试无误后点击 `Connect` ，就成功在本地远程连接上数据库
- 此时再点击 `Import` ，选择 `csv`，选择要导入的数据文件地址再点击`RUN`即可导入数据
    ![](img/3T-IMPORT.png)
    ![](img/3T-CSV.png)
    ![](img/3T-RUN.png)
    
- 成功导入数据结果如图：
  
     ![](img/3T-RESULT.png)

