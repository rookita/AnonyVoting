#!/bin/bash


function generate_blockchain_config() {
    bash ./build_chain.sh -l 127.0.0.1:4 -p 30300,20200,8545
}

function start_blockchain (){
    bash ./node/127.0.0.1/start_all.sh
}

function check_blockchain_status(){
    ps -ef | grep -v grep | grep fisco-bcos
}

function get_blockchain_logs(){
    tail -f nodes/127.0.0.1/node0/log/log*  | grep connected
}

command=$1

case $command in 
    "g"|"generate")
    generate_blockchain_config
    ;;
    "start"|"r")
    start_blockchain
    ;;
    "c")
    check_blockchain_status 
    ;;
    "l"|"logs")
    get_blockchain_logs
    ;;
    *)
    echo "wrong input !!"
esac