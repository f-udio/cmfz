import json
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import TUser
import hashlib
import datetime
from redis import Redis

redis = Redis(host='localhost', port=6379)


def get_user(request):
    rowNum = request.GET.get('rows')
    pageNum = request.GET.get('page')
    user = TUser.objects.all()
    pgntor = Paginator(user, rowNum)
    #  创建当前page对象
    pg = pgntor.page(pageNum)
    re_data = {
        "page": pageNum,
        "total": pgntor.num_pages,
        "records": pgntor.count,
        "rows": list(pg)
    }
    json_str = json.dumps(re_data, default=mydefault)
    # print(json_str)
    return HttpResponse(json_str)


def mydefault(e):
    if isinstance(e, TUser):
        h = hashlib.sha256()
        h.update(e.password.encode())
        password1 = h.hexdigest()
        if e.status == "1":
            return {'id': e.id, "username": e.username, "sex": e.sex, "phone": e.phone, "password": password1,
                    "image": str(e.image), "address": e.address, "address_item": e.address_item,
                    "signature": e.signature, "regist_time": str(e.regist_time),
                    "status": "正常"}
        return {'id': e.id, "username": e.username, "sex": e.sex, "phone": e.phone, "password": password1,
                "image": str(e.image), "address": e.address, "address_item": e.address_item, "signature": e.signature,
                "status": "冻结", "regist_time": str(e.regist_time), }


@csrf_exempt
def change_user(request):
    operation = request.POST.get('oper')
    id = request.POST.get('id')
    if operation == "edit":
        status = request.POST.get('status')
        res = TUser.objects.get(id=id)
        res.status = status
        res.save()
    elif operation == 'del':
        TUser.objects.get(id=id).delete()
    return HttpResponse('ok')


# 获取近五周的每周新增的注册人数
def get_data(request):
    data1 = redis.get("data1")
    if data1:
        data = eval(data1.decode())
        return JsonResponse(data, safe=False)
    # 当前日期
    now = datetime.datetime.now().date()
    week1 = now - datetime.timedelta(weeks=1)
    week2 = now - datetime.timedelta(weeks=2)
    week3 = now - datetime.timedelta(weeks=3)
    week4 = now - datetime.timedelta(weeks=4)
    week5 = now - datetime.timedelta(weeks=5)
    count1 = TUser.objects.filter(regist_time__gte=week1, regist_time__lt=now).count()
    count2 = TUser.objects.filter(regist_time__gte=week2, regist_time__lt=week1).count()
    count3 = TUser.objects.filter(regist_time__gte=week3, regist_time__lt=week2).count()
    count4 = TUser.objects.filter(regist_time__gte=week4, regist_time__lt=week3).count()
    count5 = TUser.objects.filter(regist_time__gte=week5, regist_time__lt=week4).count()
    data = {
        "x": [str(now) + "至" + str(week1), str(week1) + "至" + str(week2), str(week2) + "至" + str(week3),
              str(week3) + "至" + str(week4), str(week4) + "至" + str(week5)],
        "y": [count1, count2, count3, count4, count5]
    }
    redis.setex("data1", 24 * 3600, str(data))
    return JsonResponse(data)


def get_map(request):
    data = redis.get("data2")
    if data:
        data = eval(data.decode())
        return JsonResponse(data, safe=False)
        # 通过用户的地区字段进行查询并求数量   地区必须直辖市或者省
    c1 = TUser.objects.filter(address="北京").count()
    c2 = TUser.objects.filter(address="天津").count()
    c3 = TUser.objects.filter(address="上海").count()
    c4 = TUser.objects.filter(address="重庆").count()
    c5 = TUser.objects.filter(address="河北").count()
    c6 = TUser.objects.filter(address="河南").count()
    c7 = TUser.objects.filter(address="云南").count()
    c8 = TUser.objects.filter(address="辽宁").count()
    c9 = TUser.objects.filter(address="湖南").count()
    c10 = TUser.objects.filter(address="安徽").count()
    c11 = TUser.objects.filter(address="山东").count()
    c12 = TUser.objects.filter(address="新疆").count()
    c13 = TUser.objects.filter(address="江苏").count()
    c14 = TUser.objects.filter(address="浙江").count()
    c15 = TUser.objects.filter(address="江西").count()
    c16 = TUser.objects.filter(address="湖北").count()
    c17 = TUser.objects.filter(address="广西").count()
    c18 = TUser.objects.filter(address="甘肃").count()
    c19 = TUser.objects.filter(address="山西").count()
    c20 = TUser.objects.filter(address="陕西").count()
    c21 = TUser.objects.filter(address="吉林").count()
    c22 = TUser.objects.filter(address="福建").count()
    c23 = TUser.objects.filter(address="贵州").count()
    c24 = TUser.objects.filter(address="广东").count()
    c25 = TUser.objects.filter(address="青海").count()
    c26 = TUser.objects.filter(address="西藏").count()
    c27 = TUser.objects.filter(address="四川").count()
    c28 = TUser.objects.filter(address="宁夏").count()
    c29 = TUser.objects.filter(address="海南").count()
    c30 = TUser.objects.filter(address="台湾").count()
    c31 = TUser.objects.filter(address="香港").count()
    data = [
        {"name": '北京', "value": c1},
        {"name": '天津', "value": c2},
        {"name": '上海', "value": c3},
        {"name": '重庆', "value": c4},
        {"name": '河北', "value": c5},
        {"name": '河南', "value": c6},
        {"name": '云南', "value": c7},
        {"name": '辽宁', "value": c8},
        {"name": '湖南', "value": c9},
        {"name": '安徽', "value": c10},
        {"name": '山东', "value": c11},
        {"name": '新疆', "value": c12},
        {"name": '江苏', "value": c13},
        {"name": '浙江', "value": c14},
        {"name": '江西', "value": c15},
        {"name": '湖北', "value": c16},
        {"name": '广西', "value": c17},
        {"name": '甘肃', "value": c18},
        {"name": '山西', "value": c19},
        {"name": '陕西', "value": c20},
        {"name": '吉林', "value": c21},
        {"name": '福建', "value": c22},
        {"name": '贵州', "value": c23},
        {"name": '广东', "value": c24},
        {"name": '青海', "value": c25},
        {"name": '西藏', "value": c26},
        {"name": '四川', "value": c27},
        {"name": '宁夏', "value": c28},
        {"name": '海南', "value": c29},
        {"name": '台湾', "value": c30},
        {"name": '香港', "value": c31},
    ]
    redis.setex("data2", 24 * 3600, str(data))
    return JsonResponse(data, safe=False)
