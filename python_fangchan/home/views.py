from django.shortcuts import render,redirect,HttpResponse
# from myadmin import models
import math
# from  myadmin import check_code
import pymysql

from home import models
# Create your views here.
#
# def paging(NUM,p,counte):#paging(NUM,p,counte，url)可以带路由
#     path_a = math.ceil(counte / NUM)#计算需要显示的总页数shiyongmath.ceil函数()
#     path_html = ''
#     if counte<=11:
#         for i in range(1, path_a + 1):
#             #页数的样式
#             if i == p:
#                 path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#
#             else:
#                 path_html += '<a  href="/home/index?p=%d">%d</a>' % (i, i)
#     else:
#         if p<6:
#             for i in range(1, 12):
#                 if i == p:
#                     path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#                 else:
#                     path_html += '<a href="/home/index?p=%d">%d</a>' % (i, i)
#         elif p>path_a-6:
#             for i in range(path_a-12, path_a+1):
#                 if i == p:
#                     path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#                 else:
#                     path_html += '<a  href="/home/index?p=%d">%d</a>' % (i, i)
#         else:
#             for i in range(p-5, p+6):
#                 if i == p:
#                     path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#                 else:
#                     path_html += '<a  href="/home/index?p=%d">%d</a>' % (i, i)
#     return path_html
class Pager(object):
    def __init__(self,current_page):
        self.current_page = int(current_page)
    #把方法伪造成属性(1)
    @property
    def start(self):
        return (self.current_page-1)*10
    @property
    def end(self):
        return self.current_page*10
    def page_str(self,all_item,base_url):
        all_page, div = divmod(all_item,10)#（点击页，每页显示的页数）divmod（）函数返回的是余数 all_page是总页数
        if div > 0: #判断余数是否大于0，还是等于0
            all_page += 1
        pager_list = []
        if all_page <= 11:#如果总页数小于等于11
            start = 1 #起始页
            end = all_page#结束页就是all_page
        else:
            if self.current_page <= 6:
                start = 1
                end = 11 + 1#
            else:
                start = self.current_page - 5
                end = self.current_page + 6
                if self.current_page + 6 > all_page:
                    start = all_page - 10
                    end = all_page + 1
        #把页面动态起来传入起始和结束
        for i in range(start, end):
            #判断是否为当前页
            if i == self.current_page:
                temp = '<a style="color:red;font-size:26px;padding: 5px" href=" %s?page=%d">%d</a>' % (base_url,i,i)
            else:
                temp = '<a style="padding: 5px" href="%s?page=%d">%d</a>' % (base_url,i,i)
            # 把标签拼接然后返回给前端
            pager_list.append(temp)
        #上一页
        if self.current_page > 1:
            pre_page = '<a href=" %s?page=%d">上一页</a>' % (base_url, self.current_page - 1)#赋值上一页的地址
        else:
            # javascript:void(0) 什么都不干
            pre_page = '<a href="javascript:void(0);">上一页</a>'
        #下一页
        if self.current_page >= all_page:#all_page是总页数
            next_page = '<a href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a href=" %s?page=%d">下一页</a>' % (base_url, self.current_page + 1)#赋值下一页的地址
        pager_list.insert(0, pre_page)#将对象插入列表中
        pager_list.append(next_page)#在列表末尾添加对象
        return "".join(pager_list)#字符串内置拼接方法
        #a='dwdw'
        #b='eww'
        #c=''.join([a,b])
        #print(c)
        #dwdweww

def index(request):
    if request.method=='GET':
        current_page = request.GET.get('page',1)
        page_obj = Pager(current_page)
        #把方法改造成属性(2),这样在下面调用方法的时候就不需要加括号了
        res = models.Anjuke.objects.all()[page_obj.start:page_obj.end]#[page_obj.start:page_obj.end]使用切片拿取每页显示的固定长度的页数
        all_item = models.Anjuke.objects.all().count()
        all_item1 = models.AnjukeTj.objects.all().count()
        all_item2 = models.AnjukeBj.objects.all().count()
        all_item3 = models.AnjukeSh.objects.all().count()
        zgprice=models.Anjuke.objects.all().order_by('-price')[0:10]
        pager_str = page_obj.page_str(all_item,'/index')


        return render(request,'home/index.html',{'res':res,'pager_str':pager_str,'price':zgprice ,'all_item':all_item,'all_item1': all_item1,'all_item2': all_item2,'all_item3': all_item3})

# def index(request):
   # # 连接数据库
   #  conn=pymysql.connect(user=dbuser,passwd=dbpass,db=dbname,host=dbhost,charset='utf-8')
   #  cursor=conn.cursor()#创建游标
   #
   #  cursor.execute("select * from anjuke ")
   #  new_res=cursor.fetchall()
   # p = int(request.GET.get('p', 1))  # p是页数
   # counte = models.Anjuke.objects.all().count()  # 是数据库查到的总条数
   # NUM = 6  # 每页显示的条数
   # # url = 'man'
   # # path_html = paging(NUM, p, counte)
   # res = models.Anjuke.objects.all()[(p - 1) *  NUM:p *  NUM]  # 这里不需要.order_by('-id')倒序排列。因为拿到的内容就是倒序以后的
   # # zx = models.Anjuke.objects.all().order_by('-id')[0:5]
   # # zj = models.Anjuke.objects.all().order_by('-blue')[0:5]
   # return render(request, 'home/index.html', {"res": res,  'path_html': path_html})

# def paging(NUM, p, counte):  # paging(NUM,p,counte，url)可以带路由
#     path_a = math.ceil(counte / NUM)  # 计算需要显示的总页数shiyongmath.ceil函数()
#     path_html = ''
#     if counte <= 11:
#         for i in range(1, path_a + 1):
#                # 页数的样式
#             if i == p:
#                 path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#
#             else:
#                 path_html += '<a  href="/home/index?p=%d">%d</a>' % (i, i)
#     else:
#         if p < 6:
#             for i in range(1, 12):
#                 if i == p:
#                     path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#                 else:
#                     path_html += '<a href="/home/index?p=%d">%d</a>' % (i, i)
#         elif p > path_a - 6:
#             for i in range(path_a - 12, path_a + 1):
#                 if i == p:
#                     path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#                 else:
#                     path_html += '<a  href="/home/index?p=%d">%d</a>' % (i, i)
#         else:
#             for i in range(p - 5, p + 6):
#                 if i == p:
#                     path_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)
#                 else:
#                     path_html += '<a  href="/home/index?p=%d">%d</a>' % (i, i)
#     return path_html


    # 取得当前页数
    # cur_page = int(request.GET.get('p', 1))  # 第一次展示列表页数数据时没有p参数默认是1
    # NUM = 6 # 每页显示的会员信息数据条数，可设置
    # COUNT = models.Anjuke.objects.count()  # 总的会员信息记录条数
    # page = math.ceil(COUNT / NUM)  # 调用math.ceil()函数来计算出需要显示的所有总页数
    # # 页数的样式
    # page_html = ''  # 空字符串
    # # select limit()
    # for i in range(1, page + 1):
    #     # 当前页
    #     if i == cur_page:
    #         page_html += '<a class="curpage" href="/home/index?p=%d">%d</a>' % (i, i)  # 如果当前页和请求一致。显示的页数为样式设置的颜色
    #     else:
    #         page_html += '<a href="/home/index?p=%d">%d</a>' % (i, i)  # 否则显示的页数没有加样式
    # res = models.Anjuke.objects.all()[(cur_page - 1) * NUM:cur_page * NUM]
    # #读取所有列表信息，并倒序排序
    # # count_res = models.Anjuke_Bj.objects.all().order_by('-count')[0:6]
    # # sort_res=models.Anjuke_bj.objects.all().order_by('-sort')[0:4]
    #
    #
    # return render(request, 'home/index.html', {'res':res,'page_html': page_html})


def article(request):
    # if request.method=='GET':
    id = request.GET.get('id')

    res = models.Anjuke.objects.get(id=id)


    a_res = models.Anjuke .objects.filter(id__lt=id).all().order_by('-id')[0:1]#id_lt=id取得是小于当前id的数据是一个二维数据
    c = models.Anjuke .objects.filter(id__gt=id).all().order_by('id')[0:1]#id_lt=id取得是大于当前id的数据是一个二维数据
    rew= models.Anjuke.objects.filter(id__gt=id).all().order_by('id')[0:8]
    zgprice = models.Anjuke.objects.all().order_by('-price')[0:10]
    return render(request, 'home/article.html',{'res':res,'a_res':a_res,'c':c,'price':zgprice,'rew':rew })


def article1(request):
    if request.method=='GET':

        current_page = request.GET.get('page',1)
        page_obj = Pager(current_page)
        #把方法改造成属性(2),这样在下面调用方法的时候就不需要加括号了
        res = models.AnjukeTj.objects.all()[page_obj.start:page_obj.end]
        all_item= models.AnjukeTj.objects.all().count()
        all_item1 = models.Anjuke.objects.all().count()
        all_item2 = models.AnjukeBj.objects.all().count()
        all_item3 = models.AnjukeSh.objects.all().count()
        zgprice = models.AnjukeTj.objects.all().order_by('-price')[0:10]
        pager_str = page_obj.page_str(all_item,'/article1')

        return render(request,'home/article1.html',{'res':res,'pager_str':pager_str,'price':zgprice,'all_item': all_item,'all_item1': all_item1,'all_item2': all_item2,'all_item3': all_item3})


def tianjin(request):
    id = request.GET.get('id')
    res = models.AnjukeTj.objects.get(id=id)
    a_res = models.AnjukeTj.objects.filter(id__lt=id).all().order_by('-id')[0:1]  # id_lt=id取得是小于当前id的数据是一个二维数据
    c = models.AnjukeTj.objects.filter(id__gt=id).all().order_by('id')[0:1]  # id_lt=id取得是大于当前id的数据是一个二维数据
    rew = models.AnjukeTj.objects.filter(id__gt=id).all().order_by('id')[0:8]
    zgprice = models.AnjukeTj.objects.all().order_by('-price')[0:10]
    return render(request, 'home/tianjin.html', {'res': res, 'a_res': a_res,'price':zgprice,'c': c,'rew':rew})


def article2(request):
    if request.method=='GET':

        current_page = request.GET.get('page',1)
        page_obj = Pager(current_page)
        #把方法改造成属性(2),这样在下面调用方法的时候就不需要加括号了
        res = models.AnjukeBj.objects.all()[page_obj.start:page_obj.end]
        all_item = models.AnjukeBj.objects.all().count()
        all_item1 = models.Anjuke.objects.all().count()
        all_item2 = models.AnjukeTj.objects.all().count()
        all_item3 = models.AnjukeSh.objects.all().count()
        zgprice = models.AnjukeBj.objects.all().order_by('-price')[0:10]
        pager_str = page_obj.page_str(all_item,'/article2')

        return render(request,'home/article2.html',{'res':res,'pager_str':pager_str,'price':zgprice,'all_item': all_item,'all_item1': all_item1,'all_item2': all_item2,'all_item3': all_item3})

def beijing(request):
    id = request.GET.get('id')
    res= models.AnjukeBj.objects.get(id=id)
    a_res = models.AnjukeBj.objects.filter(id__lt=id).all().order_by('-id')[0:1]  # id_lt=id取得是小于当前id的数据是一个二维数据
    c = models.AnjukeBj.objects.filter(id__gt=id).all().order_by('id')[0:1]  # id_lt=id取得是大于当前id的数据是一个二维数据
    rew = models.AnjukeBj.objects.filter(id__gt=id).all().order_by('id')[0:8]
    zgprice = models.AnjukeBj.objects.all().order_by('-price')[0:10]
    return render(request, 'home/beijing.html', {'res': res, 'a_res': a_res,'price':zgprice,'c': c,'rew':rew})


def article3(request):
    if request.method == 'GET':
        current_page = request.GET.get('page', 1)
        page_obj = Pager(current_page)
        # 把方法改造成属性(2),这样在下面调用方法的时候就不需要加括号了
        res = models.AnjukeSh.objects.all()[page_obj.start:page_obj.end]
        all_item = models.AnjukeSh.objects.all().count()
        all_item1 = models.Anjuke.objects.all().count()
        all_item2 = models.AnjukeTj.objects.all().count()
        all_item3 = models.AnjukeBj.objects.all().count()
        zgprice = models.AnjukeSh.objects.all().order_by('-price')[0:10]
        pager_str = page_obj.page_str(all_item,'/article3')

        return render(request, 'home/article3.html', {'res': res, 'pager_str': pager_str,'price':zgprice,'all_item': all_item,'all_item1': all_item1,'all_item2': all_item2,'all_item3': all_item3})

def shanghai(request):
    id = request.GET.get('id')
    res= models.AnjukeSh.objects.get(id=id)
    a_res = models.AnjukeSh.objects.filter(id__lt=id).all().order_by('-id')[0:1]  # id_lt=id取得是小于当前id的数据是一个二维数据
    c = models.AnjukeSh.objects.filter(id__gt=id).all().order_by('id')[0:1]  # id_lt=id取得是大于当前id的数据是一个二维数据
    rew = models.AnjukeSh.objects.filter(id__gt=id).all().order_by('id')[0:8]
    zgprice = models.AnjukeSh.objects.all().order_by('-price')[0:10]
    return render(request, 'home/shanghai.html',{'res': res, 'a_res': a_res,'price':zgprice,'c': c,'rew':rew})




#获得验证码
def get_code(request):
    #from . import check_code#将Monaco.ttf放在根目录下
    #调用create_validate_code生成验证码，返回一个image对象，一个随机数
    img,code=check_code.create_validate_code()
    #将生成的验证码放到session中保存
    request.session['code']=code
    #使用img对象的save方法（参数1：保存图片地址）
    img_addr='static/11.png'
    img.save(img_addr)
    return HttpResponse(open(img_addr,'rb').read())

#检测验证码
def check_code(request):
    code = request.GET.get('code')
    if code.upper() == request.session.get('code').upper():
        return HttpResponse(0)
    else:
        return HttpResponse(1)



#留言内容添加到数据库
def message(request):
      if request.method=='GET':
        return render(request,'home/message.html')
      else:
           data={}
           data['my_name']=request.POST.get('my_name')
           data['content'] =request.POST.get('content')
           # code= request.POST.get('code')
           # if code.upper()!=request.session.get('code').upper():
           #     return HttpResponse(1)
           # else:
           #     return HttpResponse(0)
           models.message.objects.create(**data)#把数据插入数据表message
           return redirect( '/newlist')

#
# #留言内容添加到数据库
# def home_message(request):
#     code = request.POST.get('code')
#     if code.upper() != request.session.get('code').upper():
#         return HttpResponse(1)
#     else:
#         data = {}
#         data['name'] = request.POST.get('name')
#         data['content'] = request.POST.get('content')
#         models.message.objects.create(**data)
#         return HttpResponse(0)

def newlist(request):
    # 取得当前页数
    cur_page = int(request.GET.get('p', 1))  # 第一次展示列表页数数据时没有p参数默认是1
    NUM = 5 # 每页显示的会员信息数据条数，可设置
    COUNT = models.message.objects.count()  # 总的会员信息记录条数
    page = math.ceil(COUNT / NUM)  # 调用math.ceil()函数来计算出需要显示的所有总页数
    # 页数的样式
    page_html = ''  # 空字符串
    for i in range(1, page + 1):
        # 当前页
        if i == cur_page:
            page_html += '<a class="curpage" href="/home/newlist?p=%d">%d</a>' % (
                i, i)  # 如果当前页和请求一致。显示的页数为样式设置的颜色
        else:
            page_html += '<a href="/home/newlist?p=%d">%d</a>' % (i, i)  # 否则显示的页数没有加样式
    res = models.message.objects.all().order_by('-id')[(cur_page - 1) * 5:cur_page * 5]
    return render(request, 'home/newlist.html', {'res': res,'page_html':page_html})


