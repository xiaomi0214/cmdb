
#!/bin/bash

python2_Mode=( requests  psutil argparse)

##1.准备dns解析服务器
echo "nameserver 114.114.114.114" >>/etc/resolv.conf

##2.更新源
yum install wget -y
cd /etc/yum.repos.d
mkdir repobak
mv *.repo repobak
wget http://ftp.loongnix.org/os/loongnix/1.0/fedora.repo
yum clean all
yum makecache fast


##3.安装基础包
##python-devel
rpm -aq |grep python-devel >>/dev/null
if [[ $? != 0 ]]
then
yum install python-devel -y
fi

##gcc-c++
rpm -aq |grep gcc-c++ >>/dev/null
if [[ $? != 0 ]]
then
yum install gcc-c++ -y
fi

##pip
which pip
if [[ $? != 0 ]]
then
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py ;python get-pip.py
fi


for  mod in ${python2_Mode[@]}
do
	pip install $mod  >>/dev/null
	python -c "import $mod"
	if [[ $? != 0 ]]
	then
		echo "$mod 安装失败"
		exit
	fi
done

echo "基础环境准备完成"


echo "基础环境准备完成"
