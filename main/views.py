from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from cpx_cmfz import settings
from utils.send_message import YunPian
from utils.rondom_code import Getcode
from redis import Redis
import re

Rs = Redis(
    host='localhost',
    port=6379,
)


# 登录页面
def login(request):
    return render(request, 'login.html')


# 首页
def index(request):
    if request.session.get('dl'):
        return render(request, "main.html")
    return redirect('main:login')


# 用户获取短信
@csrf_exempt
def get_code(request):
    mobile = request.POST.get('mobile')
    mobile_ok = re.match(r"^1[35678]\d{9}$", mobile)
    code = request.POST.get('code')
    print(code)
    # 查看冷却
    if Rs.get(mobile + '.'):
        return HttpResponse('频繁获取，冷却中')
    else:
        # 判断手机格式是否正确
        if mobile_ok:
            # 根据获取到手机号去发送短信
            yunpian = YunPian(settings.APIKEY)
            # 生成六位验证码
            code = Getcode().getcode()
            # 向该号码发送验证码
            yunpian.send_message(mobile, code)
            # 存冷却时间
            Rs.set(mobile + '.', code, 60)
            # 存有效时间
            Rs.set(mobile + '..', code, 1800)

        return HttpResponse('手机格式错误')


# 登陆逻辑
@csrf_exempt
def check_user(request):
    mobile = request.POST.get('mobile')
    code = request.POST.get('code')
    mobile_ok = re.match(r"^1[35678]\d{9}$", mobile)
    if mobile_ok:

        a = Rs.get(mobile + '..')
        # 判断验证码是否还处在有限期且与用户输入验证码相同
        if a and a.decode() == code:
            request.session['login'] = True
            return HttpResponse('登陆成功...')
        return HttpResponse('登陆失败，请重新验证...')
    return HttpResponse('手机号输入错误...')
