## 简介
AnnoyVote是一块基于区块链的多场景的可定制化的匿名投票平台，旨在解决“黑幕式投票”的痛点问题。

## 依赖
+ python3.7+
+ FISCO BCOS 2.x
+ @vue/cli 5.0.6 & yarn version v1.22.18

## 使用方法
1.按照[FISCO](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/index.html)的教程搭建一个区块链网络并下载fisco的python-sdk。

2.在blockchain.py中添加python-sdk的路径（第11行）。

3.`cd avecvoting && pip install -r requirements.txt`安装python依赖。

4.`python app.py`启动后端。

5.`cd vue-web &&  yarn install && yarn serve`启动前端。

6.127.0.0.1:8081端口可进入投票平台。

## 其他
1.可使用gunicorn封装flask后端。
2.若需要用nginx，请将vue-web中的dist文件夹移动至nginx默认html文件夹(/var/www/html)。
3.如有问题联系dl191@mail.ustc.edu.cn。