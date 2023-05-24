#!/bin/bash
function infolog(){
    echo
    echo -e "\033[32m$@\033[0m"
    echo
}


infolog "编译并部署合约"
python blockchain.py

infolog "启动flask"
python app.py