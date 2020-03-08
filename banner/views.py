from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, HttpResponse
from banner.models import Bnner
import json
from django.views.decorators.csrf import csrf_exempt


# 存储轮播图
@csrf_exempt
def save_banner(request):
    try:
        # 获取名称
        title = request.POST.get('title')
        # 获取状态
        status = request.POST.get('status')
        # 获取文件
        pic = request.FILES.get('pic')
        print(title, status, pic)
        if not pic:
            # pic 不存在
            return HttpResponse("图片不能为空")
        # 存入数据库
        with transaction.atomic():
            Bnner.objects.create(title=title, status=status, pic=pic)
        return HttpResponse('成功保存')
    except:
        return HttpResponse('保存失败')


# 序列化所有默认函数
def my_default(b):
    if isinstance(b, Bnner):
        return {'id': b.id, 'title': b.title, 'status': b.status, 'create_time': str(b.create_time), 'pic': str(b.pic)}


# 展示轮播图数据
def show_banner(request):
    print(Bnner.objects.get(pk=1).pic)
    # 从前端获取每页显示行数
    row_num = request.GET.get('rows')
    # 从前端获取页码
    page_num = request.GET.get('page')
    # 从数据库获取数据 进行分页管理
    pgtor = Paginator(Bnner.objects.all(), per_page=row_num)
    # 生成page
    pg = pgtor.page(page_num)
    # 返回的数据
    data = {
        'page': page_num,
        'total': pgtor.num_pages,
        'records': pgtor.count,
        'rows': list(pg)
    }
    # 进行序列化
    json_str = json.dumps(data, default=my_default)
    return HttpResponse(json_str)


# 编辑轮播图列表
@csrf_exempt
def edit_banner(request):
    try:
        # 获取oper,添，修改edit，删除del
        oper = request.POST.get('oper')
        print(oper)
        # 判断是修改，还是删除
        if oper == 'edit':
            # 修改 , 获取 需要修改的数据
            id = request.POST.get('id')
            title = request.POST.get('title')
            status = request.POST.get('status')
            # 通过id获取modal对象
            banner = Bnner.objects.get(pk=id)
            # 进行修改
            with transaction.atomic():
                banner.title = title
                banner.status = status
                banner.save()
            return HttpResponse('成功修改')
        elif oper == 'del':
            # 获取id
            id = request.POST.get('id')
            # 从数据库删除
            Bnner.objects.get(pk=id).delete()
            return HttpResponse('成功删除')
    except:
        return HttpResponse('操作失败')
