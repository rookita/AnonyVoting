# AvecVoting

区块链电子投票实现

## 环境搭建

### **启动区块链**
```sh
mkdir evoting && cd evoting
curl -LO https://github.com/FISCO-BCOS/FISCO-BCOS/releases/download/v2.8.0/build_chain.sh && chmod u+x build_chain.sh #下载脚本
bash build_chain.sh -l 127.0.0.1:4 -p 30300,20200,8545 #部署4个节点
./nodes/127.0.0.1/start_all.sh #启动所有节点
```

### **部署Python-SDK**

```
cd ~
git clone https://github.com/FISCO-BCOS/python-sdk #克隆仓库
cd python-sdk
pip install -r requirements.txt 
bash init_env.sh -i
npm install solc@v0.4.25
cp ~/evoting/nodes/127.0.0.1/sdk/* ./bin #复制证书
```
测试 Python SDK 和节点的连通性
```sh
./console.py getNodeVersion #检查SDK能否连接节点。
```

### 项目部署

```sh
cd evoting
git clone  git@git.lug.ustc.edu.cn:oliver/avecvoting #拉取源代码
cd avec && pip install -r requirement.txt
cp -r ${PATH_TO_PYTHON_SDK}/bin/* ./bin #将python-sdk的bin文件夹内容复制bin中
python blockchain.py    #编译部署合约
python app.py           #启动flask服务
```

### WeBASE部署

WeBASE 提供了方便的智能合约开发和调试平台，本节内容介绍 WeBASE 的部署方案。

#### Mysql 数据库部署
使用如下命令部署 Mysql 数据库：

```sh
docker pull mysql:5.6
sudo apt install mariadb-client-core-10.1 
pip3 install PyMySQL
```

#### WeBASE 

使用如下命令即可获取 WeBase 代码并配置相关文件：

```sh
wget https://osp-1257653870.cos.ap-guangzhou.myqcloud.com/WeBASE/releases/download/v1.5.3/webase-deploy.zip
unzip webase-deploy.zip && cd webase-deploy
mkdir sqlConf sqlData sqlLogs
docker run -p 3306:3306 --name mysql56 -v $PWD/sqlConf:/etc/mysql/conf.d -v $PWD/sqlLogs:/logs -v $PWD/sqlData:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6
```

我们注意到，需要修改 `webase-deploy/comm/check.py`, 将 47 行 `checkExitedChainInfo()` 注释掉。否则 WeBASE 无法运行。

#### 修改commom-properties 配置文件
我们需要进一步配置 WeBASE的相关信息，用于数据库接入等。

``` sh
# Mysql database configuration of WeBASE-Node-Manager
mysql.ip=127.0.0.1
mysql.port=3306
mysql.user=root
mysql.password=123456
mysql.database=webasenodemanager

# Mysql database configuration of WeBASE-Sign
sign.mysql.ip=127.0.0.1
sign.mysql.port=3306
sign.mysql.user=root
sign.mysql.password=123456
sign.mysql.database=webasesign

# 为防止端口冲突，将5001-5004改为5100-5104
# WeBASE-Web service port 
web.port=5100

# WeBASE-Node-Manager service port
mgr.port=5101

# WeBASE-Front service port
front.port=5102

# WeBASE-Sign service port
sign.port=5104

# 由于使用已有区块链节点，故设置一下参数
if.exist.fisco=yes
fisco.dir=/home/ubuntu/evoting/nodes/127.0.0.1
```
#### 启动 WeBASE 组件

使用如下命令启动 WeBASE 组件。

```sh
python deploy.py installAll # 启动WeBASE服务
```
