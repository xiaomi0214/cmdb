#!/bin/bash 

jiagou=`uname -m`

case ${jiagou} in 
"aarch64")
	bash -x arm/ready.sh;;
"x86_64")
	bash -x x86/ready.sh;;
"mips64")
	bash -x mips/ready.sh;;
*)
	echo "获取服务器架构失败。。"
	exit ;;
esac

if [ $? -eq 0 ]
then 
	python monitoy.py
fi 
