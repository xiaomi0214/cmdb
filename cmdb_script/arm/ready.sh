
#!/bin/bash

python2_Mode=( requests  psutil argparse)

##1.准备dns解析服务器
echo "nameserver 114.114.114.114" >>/etc/resolv.conf

##2.更新源
mv /etc/apt/sources.list /etc/apt/sources.list.bak
cat >>/etc/apt/sources.list<<EOF
deb ftp://192.168.2.32/pub/FT/kord-juniper juniper main universe multiverse restricted
deb http://mirrors.163.com/debian/ stretch main non-free contrib
deb http://mirrors.163.com/debian/ stretch-updates main non-free contrib
deb http://mirrors.163.com/debian/ stretch-backports main non-free contrib
deb http://mirrors.163.com/debian-security/ stretch/updates main non-free contrib
EOF

apt update
##3.安装基础包
apt-get install python-dev -y

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
