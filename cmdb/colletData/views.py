from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
# Create your views here.
import json
from cmdb.models import *

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def server(request):
    if request.method == "POST":
        print(request.method)
        print(request.body)

        bodyData = json.loads(request.body)
        try:
            cpu_jg = bodyData.get('bootinf').get('cpu_result')
            cpu_type = bodyData.get('cpuinf').get('cpu_type')
            cpu_count = bodyData.get('cpuinf').get('cpu_count')

            memory_size = bodyData.get('memoryinf').get('mem_total')
            root_size = bodyData.get('diskinf').get('disk_total')

            czxt = bodyData.get('bootinf').get('czxt')
            hostname = bodyData.get('systeminf').get('hostname')

            create_time = bodyData.get('cur_time')

            ipv4 = bodyData.get('netinf').get('inter_ipv4_addr')
            macaddr = bodyData.get('netinf').get('inter_mac_addr')

            adminId= bodyData.get('deplyInf').get('adminId')
            userPeople=bodyData.get('deplyInf').get('user')
            localtion = bodyData.get('deplyInf').get('localtion')
            application = bodyData.get('deplyInf').get('application')


        except Exception as error:
            print(error)
            # return HttpResponse("获取数据失败，原因：%s"%error)
            result = {
                "status": "false",
                "mesage": error
            }
            return Response(result)
        ##获取网络信息
        else:
            list = Server.objects.filter(mac=macaddr)
            print(list, len(list))
            if len(list) != 0:
                return Response({"status": "false", "mesage": "机器已经添加"})
                # return HttpResponse("机器已经添加！")

            eoplepObj=People.objects.filter(id=int(adminId))
            if len(eoplepObj)==0:
                print("管理员账号不存在")
                return Response({"status": "false", "mesage": "管理员账号不存在"})
            server = Server(
                cpu_jg=cpu_jg,
                cpu_type=cpu_type,
                cpu_count=cpu_count,
                memory_size=memory_size,
                root_size=root_size,
                czxt=czxt,
                hostname=hostname,
                create_time=datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S"),
                mac=macaddr,
                ipv4=ipv4,
                localtion=localtion,
                use_people=userPeople,
                application=application,
                admin=eoplepObj[0]
            )

            server.save()
            return Response({"status": "success", "mesage": "{ip} 机器添加成功".format(ip=ipv4)})
    elif request.method == "GET":
        serverList = Server.objects.all()
        print(len(serverList))
        serList = []
        if len(serverList) == 0:
            return Response('')
        for server in serverList:
            serList.append({
                "ipv4": server.ipv4,
                "hostname": server.hostname,
                "cpu_jg": server.cpu_jg,
                "cpu_count": server.cpu_count,
                "memory_size": server.memory_size,
                "cpu_type": server.cpu_type,
                "root_size": server.root_size,
                "czxt": server.czxt,
                "create_time": server.create_time,
                "mac": server.mac
            })
            # print(serSET)
        return Response({"status": "success", "data": serList})
    # elif request.method == "DELETE":
    #     pass


@api_view(['GET'])
def getIps(request):
    if request.method == "GET":
        serverList = Server.objects.all()
        if len(serverList) == 0:
            return Response('')
        ipList = []
        for server in serverList:
            ipList.append(server.ipv4)
        return Response({"status": "success", "data": ipList})
