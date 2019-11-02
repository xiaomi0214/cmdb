
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
import json
from cmdb.models import *
from django.shortcuts import render,redirect
import socket
import time



def signIn(request):
    """
    nichen = models.CharField(unique=True, max_length=30)
    email = models.CharField(unique=True, max_length=30)
    passwd = models.CharField(max_length=50)
    isready = models.IntegerField()
    :param request:
    :return:
    """
    if request.method=="POST":
        name=request.POST.get('name')
        passwd=request.POST.get('password')
        msg="昵称和密码不能为空"
        if name and passwd:
            obj=People.objects.filter(nichen=name,passwd=passwd)
            if not obj:
                msg="昵称和密码不正确"
            else:
                request.session['loginStatus'] = 'true'
                request.session['name'] = name
                return redirect('/')

        return HttpResponse(msg)
    return  render(request,'sign_in.html')

def checkLogin(func):
    def gateFunc(request):
        loginStatus=request.session.get('loginStatus','')
        if not loginStatus:
            return redirect('/login/')
        else:
            return func(request)
    return gateFunc


@checkLogin
def signOut(request):
    del request.session['loginStatus']
    return redirect('/login/')



@checkLogin
def index(request):
    name=request.session.get('name')
    print(name)
    return render(request,'index1.html',{"name":name})

def serverList(request):
    #form_styles.html
    name=request.session.get('name')
    if request.method=="POST":
        jiagou = request.POST.get('jiagou')
        czxt = request.POST.get('czxt')
        use = request.POST.get('use')
        print("检索的信息：{jiagou}  {czxt}  {use}".format(jiagou=jiagou,czxt=czxt,use=use))

        #servers = Server.objects.filter(cpu_jg__contains=jiagou,czxt__contains=czxt,use__contains=use)
        servers = Server.objects.filter(cpu_jg__contains=jiagou)
        serverList = []
        print("检索到服务器的个数：{num}".format(num=len(servers)))
        if len(servers) != 0:
            for server in servers:
                print( type(server.admin))
                # print(server.admin,type(server.admin),People.objects.get(id=server.admin))
                # People.objects.get(id=server.admin).nichen
                serverList.append({
                    "ipv4": server.ipv4,
                    "cpu_jg": server.cpu_jg,
                    "czxt": server.czxt,
                    "create_time": server.create_time,
                    "use_people": server.use_people,
                    "use": server.application,
                    "admin": server.admin.nichen,
                    "localtion": server.localtion
                })

        return render(request, 'serverList.html', {"datas": serverList, "name": name})
    elif request.method=="GET":
        return render(request, 'serverList.html', {"name": name})



@checkLogin
def descServer(request):
    name=request.session.get('name')

    print(request.GET)
    ip=request.GET.get('ip')
    if not ip:
        return HttpResponse("传参有误")
    server=Server.objects.get(ipv4=ip)
    print(server,type(server))
    datas={
        "ip":ip,
        "cpu_count": server.cpu_count,
        "cpu_type": server.cpu_type,
        "memory_size": server.memory_size,
        "root_size": server.root_size,
        "hostname": server.hostname,
    }
    return render(request,'descServer.html',{"datas":datas,"name":name})


def getcmdbip():
    serverList = Server.objects.all()
    ipList = []
    if len(serverList) != 0:
        for server in serverList:
            ipList.append(server.ipv4)
    return ipList

#获取申请表的ip列表

def getapplyip():
    ipObjs = Applyip.objects.all()
    ipsList = []
    if len(ipObjs) != 0:
        for ipObj in ipObjs:
            ipsList.append(ipObj.ip)
    return ipsList

def getuserdip():
    cmdbipList=getcmdbip()
    print("获取cmdbip：{cmdbipList}".format(cmdbipList=cmdbipList))
    applyipLiast=getapplyip()
    print("获取applyip：{applyipLiast}".format(applyipLiast=applyipLiast))
    useripSet=set(cmdbipList)|set(applyipLiast)
    print("已经使用的ip列表：{useripSet}".format(useripSet=useripSet))
    return useripSet


def getallIp(netSegment):
    """
    获取某个网段的全部ip
    参数：网段(networkSegment)，形如192.168.2.0
    :return:这个网段所有ip的集合192.168.2.1-254
    """
    # netSegment = "192.168.2.0"
    # num = 5
    nets = '.'.join(netSegment.split('.')[:3])
    netsIpsSet = set([nets + ".{i}".format(i=i) for i in range(1, 255)])
    return netsIpsSet

def getUnUseIpSet(netSegment):
    netSegSet=getallIp(netSegment)
    useipSet = getuserdip()
    unUseipSet = netSegSet - useipSet
    return unUseipSet

@checkLogin
def applyIps(request):
    name=request.session.get('name')
    msg=""
    if request.method=="POST":
        # ##获取cmdb 中的ip

        """
        <QueryDict: {'netSegment': ['192.168.2.0'], 'ipNum': ['10']}>
        """
        #获取参数
        ipLists = ""
        status = False

        netSegment = request.POST.get('netSegment')
        ipNum = request.POST.get('ipNum')
        print("接受的参数：netSegment:{netSegment},ipNum:{ipNum}".format(netSegment=netSegment,ipNum=ipNum))
        try:
            ipNum=int(ipNum)
        except Exception as error:
            msg="参数不为空且只能数字"
            return render(request,'applyIp.html',{"name":name,"msg":msg})
            # return HttpResponse("status:{status},错误信息：{msg}".format(status=status,msg=msg))
        if ipNum<=0:
            msg = "申请ip数目只能是正整数"
            return render(request, 'applyIp.html', {"name": name, "msg": msg})
        unUseipSet=getUnUseIpSet(netSegment)
        unUseIps = sorted(list(unUseipSet), key=socket.inet_aton)

        if len(unUseIps)<int(ipNum):
            msg="本网段ip不足，现有ip数量：{ipnum}".format(ipnum=len(unUseIps))
        else:
            msg="获取ip成功"
            ipLists=unUseIps[:ipNum]
            stats=True

        print("获取ip结果：{msg}  \nip列表:{ips}".format(msg=msg,ips=ipLists))
        return render(request, 'applyIp.html',{"datas":{"status":stats,"ips":ipLists},'name':name,"msg":msg})

    elif request.method=="GET":
        return render(request, 'applyIp.html',{'name':name,"msg":msg})

@checkLogin
def applyIpConfirm(request):
    if request.method == "POST":
        msg="申请ip成功"
        name=request.session.get('name')
        user=People.objects.get(nichen=name)

        print(request.POST)
        ipStr = request.POST.get('iplist')


        print("确认的ip列表：{iplist}".format(iplist=ipStr))

        if ipStr=="":
            msg="提交数据为空"
            return render(request, 'applyIp.html', {'name': name, "msg": msg})
            # return HttpResponse(msg)
        applyIpList=[]
        # print(type(iplist),iplist.split('\r\n\t\t\t\r\n\t\t\t'))
        ipStr=ipStr.replace('\t', '').replace('\r', '').replace('\n', ' ')
        iplist=[ip.strip(' ') for ip in ipStr.split(' ')]
        print(iplist)
        applySuccessIp=[]
        for ip in iplist:
            print(ip)
            if ip :
                ApplyipObjList=Applyip.objects.filter(ip=ip)
                if len(ApplyipObjList)==0 :
                    obj=Applyip(
                        uid=user,
                        ip=ip,
                        applytime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    )
                    obj.save()
                    print("记录ip:{ip}".format(ip=ip))
                    applySuccessIp.append(ip)
                else:
                    print("此ip已在申请表中:{ip}".format(ip=ip))
                    msg="此ip已在申请表中"
                    # return render(request, 'applyIp.html', {'name': name, "msg": msg})
                    # return HttpResponse(msg)

        return render(request,'applyIp.html',{"name":name,"msg":msg,"datas":{"ips":applySuccessIp}})
        # return HttpResponse(msg)


def getApplyIps(name):
    obj = People.objects.get(nichen=name)
    ipsObjs = Applyip.objects.filter(uid=obj)
    print(ipsObjs)
    ipsList = []
    if len(ipsObjs) != 0:
        for ipsObj in ipsObjs:
            ipsList.append({
                "ip": ipsObj.ip,
                "date": ipsObj.applytime
            })
    return ipsList

@checkLogin
def applydIps(request):
    name=request.session.get('name')
    ipsList=getApplyIps(name)
    return render(request,"applydIps.html",{"ipsList":ipsList,"name":name})
@checkLogin
def deleteIp(request):
    name = request.session.get('name')
    ip=request.GET.get("ip")
    print("需要删除的申请ip:{ip}".format(ip=ip))
    ##删除申请表信息
    obj=Applyip.objects.get(ip=ip)
    obj.delete()

    servObj=Server.objects.filter(ipv4=ip)
    if len(servObj)!=0:
        servObj[0].delete()
    ipsList = getApplyIps(name)
    return render(request,"applydIps.html",{"ipsList":ipsList,"name":name})


@api_view(['GET','PUT'])
def putServer(request):
    if request.method=="put":
        pass
    elif    request.method=="GET":
        serverList=Server.objects.all()
        print(len(serverList))
        serList=[]
        if len(serverList)==0:
            return Response('')
        for server in serverList:
            serList.append({
                "ipv4": server.ipv4,
                "hostname":server.hostname,
                "czxt":server.czxt,
                "create_time":server.create_time
            })
            # print(serSET)
        return Response({"status": "success", "data":serList})

