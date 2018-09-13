from django.shortcuts import render,HttpResponse,redirect,reverse
from myadmin import models
import math
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#用户验证装饰器
def check_cookie(func):
    def return_res(*args,**kwargs):
        print(args)
        if not args[0].COOKIES.get('username'):
            return redirect('/myadmin/login')
        else:
            return func(*args,**kwargs)
    return return_res
#md5加密函数
def str_jiami(mystr):
    #导入hashlib模块
    import hashlib
    #用模块去实例化md5加密函数创建对象
    md5=hashlib.md5()
    #调用update方式加密mystr字符串，需要将mystr转化为utf-8字节码
    md5.update(mystr.encode())
    #返回加密后的内容
    return md5.hexdigest()
#后台首页
@check_cookie#装饰器检查用户是否登录
def index(request):
    #如果存在cookie
    #if request.COOKIES.get('username'):
    return render(request,'myadmin/index.html')
    #return redirect( '/myadmin/login')#跳转使用redirect访问的网址必须是绝对路径/t跳转到后台登陆页面.重定向函数

#--------------------用户登陆start————————
#登陆方法adin
def login(request):
        #如果用户已经登陆，直接跳转到后台首页
        if request.COOKIES.get('username'):#使用request请求带上cookies,为真则
            return redirect('/myadmin/')#跳转到后台的根网址
        return render(request,'myadmin/login.html')
        # i=0
        # code=''
        # while i<4:
        #     code += str(code_str[random.randint(0,9)])
        #     i=i+1
        # request.session['code']=code
        # return render(request,'myadmin/login.html',{'code':code})
            #render()函数是访问需要渲染的页面，赋值返回到后台登陆页面，重新登陆
#获得验证码
def get_code(request):
    from . import check_code#将Monaco.ttf放在根目录下
    #调用create_validate_code生成验证码，返回一个image对象，一个随机数
    img,code=check_code.create_validate_code()
    #将生成的验证码放到session中保存
    request.session['code']=code
    #使用img对象的save方法（参数1：保存图片地址）
    img_addr='static/11.png'
    img.save(img_addr)
    return HttpResponse(open(img_addr,'rb').read())

def check_login(request):
        #取得参数
    username=request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('code')#验证验证码
        # #返回0-账号信息正确  返回1---账号信息错误 2-验证码错误
    if code.upper()!= request.session.get('code').upper():
        return HttpResponse(2)
    password=str_jiami(password)#如果已登录则，对密码加密
    res=models.admin.objects.filter(username=username,password=password).count()#把得到的数据赋值给数据库，并把数据库计算的相同用户信息数赋值给res
    if res:#如果数值为1，真则没有重复用户登陆
        response = HttpResponse(0)
        response.set_cookie('username',username,max_age=3600)#浏览器响应来设置cookie保存的当前的用户数据，和保存时间
        return response#浏览器返回响应结果
    else:
        return HttpResponse(1)
            # error = '两次输入密码不一致,跳转到错误页面'
            # return render(request, 'myadmin/error.html', {'error': error})
#退出登陆操作
def login_out(request):
    response=redirect('/myadmin/login')
    #删除cookie
    response.delete_cookie('username')
    return response#返回响应
#检查验证码
def check_code(request):
    code=request.GET.get('code')
    if code.upper()==request.session.get('code').upper():
        return HttpResponse(0)
    else:
        return HttpResponse(1)

#获得验证码
#-------------------------用户登陆end-----------------

#--------------用户管理start-----------

#管理员列表
@check_cookie#装饰器检查用户是否登录
def admin_list(request):
    #查询管理员信息
    #取得当前页数
    cur_page=int(request.GET.get('p',1))#第一次展示列表页数数据时没有p参数默认是1
    NUM=3#每页显示的会员信息数据条数，可设置
    COUNT=models.admin.objects.count()#总的会员信息记录条数
    page=math.ceil(COUNT/NUM)#调用math.ceil()函数来计算出需要显示的所有总页数
    #页数的样式
    page_html=''#空字符串
    for i in range(1,page+1):
        #当前页
        if i == cur_page:
            page_html +='<a class="curpage" href="/myadmin/admin_list?p=%d">%d</a>'%(i,i)#如果当前页和请求一致。显示的页数为样式设置的颜色
        else:
            page_html +='<a href="/myadmin/admin_list?p=%d">%d</a>' % (i,i)#否则显示的页数没有加样式
    res=models.admin.objects.all().order_by('-id')[(cur_page-1)*3:cur_page*3]#读取所有列表信息，并倒序排序
    return render(request,'myadmin/admin_list.html',{'res':res,'page_html':page_html})#返回跳转到管理员列表。并把所有管理员信息安页数显示
#管理员添加
@check_cookie
def admin_add(request):#添加函数
    if request.method=='GET':#判断点击添加后请求方式
        return render(request,'myadmin/admin_add.html')#则访问返回添加页面
    else:#当是添加完成后的post请求则
        username=request.POST.get('username')#request请求拿到的username赋值给username
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        if password==repassword:#判断添加新管理员的密码和确认密码一致
            count=models.admin.objects.filter(username=username).count()
            #对用户名不能重复进行判断
            if not count:
                password=str_jiami(password)#对拿到的管理员用md5加密函数来# 密码加密
                models.admin.objects.create(username=username,password=password)#把新管理员信息数据保存到数据库，括号中前面的username是数据库中的字段名，后面的是post得到的管理员名称
                return redirect('/myadmin/admin_list')#然后返回跳转到管理员列表页面完成新管理员添加，redirect是跳转到地址，前面必须加/
                #return redirect(reverse('admin_list'))#添加新管理员完成后返回到后台管理员列表页面
            else:
                error ='用户名已存在'
                return render(request,'myadmin/error.html',{'error':error})
        else:
            error='两次输入密码不一致'
            return render(request,'myadmin/error.html',{'error':error})#返回到错误页面，带参数error显示的是错误内容

##修改用户信息
@check_cookie
def admin_edit(request):
    if request.method=='GET':
        #取得当前修改用户参数
        id=request.GET.get('id')
        #通过数据库查询用户信息
        res=models.admin.objects.get(id=id)
        print(res)
        return render(request,'myadmin/admin_edit.html',{'res':res})#访问返回后res参数当前用户的修改页面
    else:#取得参数
        id = request.POST.get('id')
        password= request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password == repassword :  # 判断如果修改密码和确认密码一致

            password=str_jiami(password) #加密密码
            models.admin.objects.filter(id=id).update(password=password)#数据库查找修改当前用户的密码
             # obj=models.admin.objects.get(id=id)#得到当前用户对象
             # obj.password=pwd#把输入post得到密码赋值给，用户对象的.password密码，
             # obj.save()#保存obj对象
            return redirect('/myadmin/admin_list')
        else:
            error = '两次输入密码不一致'
            return render(request, 'myadmin/error.html', {'error': error})
 # 删除管理员信息
def admin_del(request):
    id = request.GET.get('id')
    models.admin.objects.filter(id=id).delete()
    return redirect('/myadmin/admin_list')

#检查用户是否存在
def check_user(request):
    username = request.GET.get('username')
    count= models.admin.objects.filter(username=username).count()
    return HttpResponse(count)
#--------------------用户管理end————————-----

#—————————————文章分类开始————————
#分类列表
@check_cookie
def article_cat_list(request):#定义分类列表函数
    res=models.article_cat.objects.all().order_by('-id')#order_by(-1)是倒序排列#从数据库得到所有articl_cat表的信息数据
    return render(request,'myadmin/article_cat_list.html',{'res':res})#返回访问，数据库得到参数数据后，来渲染后返回到分类列表页面
#添加分类列表
@csrf_exempt
def article_cat_add(request):
    #取得参数
    cat_name=request.POST.get('cat_name')
    #插入到article数据库中
    models.article_cat.objects.create(cat_name=cat_name)
    return redirect('/myadmin/article_cat_list')
#删除分类操作
@check_cookie
def article_cat_del(request):

    id=request.GET.get('id')
    #数据库操作
    models.article_cat.objects.filter(id=id).delete()
    #页面重定向
    return redirect('/myadmin/article_cat_list')

#修改分类操作
@check_cookie
def article_cat_edit(request):
    id=request.GET.get('id')
    cat_name=request.GET.get('cat_name')
    models.article_cat.objects.filter(id=id).update(cat_name=cat_name)
    return HttpResponse('操作成功')

#——————-文章分类end————————

#----------文章start——————————
#文章列表页
def article_list(request):
    # 取得当前页数
    cur_page = int(request.GET.get('p', 1))  # 第一次展示列表页数数据时没有p参数默认是1
    NUM = 3  # 每页显示的会员信息数据条数，可设置
    COUNT = models.article.objects.count()  # 总的会员信息记录条数
    page = math.ceil(COUNT / NUM)  # 调用math.ceil()函数来计算出需要显示的所有总页数
    # 页数的样式
    page_html = ''  # 空字符串
    for i in range(1, page + 1):
        # 当前页
        if i == cur_page:
            page_html += '<a class="curpage" href="/myadmin/article_list?p=%d">%d</a>' % (
            i, i)  # 如果当前页和请求一致。显示的页数为样式设置的颜色
        else:
            page_html += '<a href="/myadmin/article_list?p=%d">%d</a>' % (i, i)  # 否则显示的页数没有加样式
    res = models.article.objects.all().order_by('-id')[(cur_page - 1) * 3:cur_page * 3]  # 读取所有列表信息，并倒序排序
    return render(request,'myadmin/article_list.html',{'res':res,'page_html':page_html})

#添加文章页
def article_add(request):
    if request.method == 'GET':
        cat_res=models.article_cat.objects.all()
    # 插入到article数据库中
        return render(request,'myadmin/article_add.html',{'cat_res':cat_res})
    else:
        data={}
        data['title']=request.POST.get('title')
        data['desc'] = request.POST.get('desc')
        data['cat_id'] = request.POST.get('cat_id')
        data['content'] = request.POST.get('content')
        data['sort'] = request.POST.get('sort')
        data['count'] = request.POST.get('count')
        image=request.FILES.get('image')
        # 判断是否上传照片
        if image:
            #取得原来照片名
            img_name=image.name
            #取得图片名
            img_type = img_name.split('.')[-1]
            #创建新照片名
            import uuid #加载uuid模块来随机生成新的生成照片名
            new_img_name=str(uuid.uuid1())+'.'+img_type
            #存储路径
            image_addr='static/upload/'+new_img_name# 这里的是相对地址，最前面不能加/
            with open(image_addr, 'wb')as f:
                f.write(image.read())

                #将图片的地址赋值给数据库中的data['image']
                data['image']='/'+image_addr
                # print(image.read())
                #把所有的个字段属性，数据写入到数据库
        models.article.objects.create(**data)
        return redirect('/myadmin/article_list')
#修改文章
def article_edit(request):
    if request.method =="GET":
        #取得id参数
        id=request.GET.get('id')
        res=models.article.objects.get(id=id)
        #取得所有的分类
        cat_res =models.article_cat.objects.all()
        return render(request,'myadmin/article_edit.html',{'res':res,'cat_res':cat_res})
    else:
        # 取得id参数
        id = request.POST.get('id')
        data = {}
        data['title'] = request.POST.get('title')
        data['desc'] = request.POST.get('desc')
        data['cat_id'] = request.POST.get('cat_id')
        data['content'] = request.POST.get('content')
        data['sort'] = request.POST.get('sort')
        data['count'] = request.POST.get('count')
        image = request.FILES.get('image')
        # 判断是否上传图片
        if image:
            # 取得原图片名
            img_name = image.name
            # 取得图片后缀
            img_type = img_name.split('.')[-1]
            # 图片新图片名
            import uuid
            new_img_name = str(uuid.uuid1()) + '.' + img_type
            # 存储路径
            image_addr = 'static/upload/' + new_img_name
            with open(image_addr, 'wb') as f:
                f.write(image.read())
            # 将图片地址赋值给添加的图片字段
            data['image'] = '/' + image_addr
        models.article.objects.filter(id=id).update(**data)
        return redirect('/myadmin/article_list')

def article_del(request):
     id = request.GET.get('id')
    # print(id)
    # 数据库操作
     models.article.objects.filter(id=id).delete()
     # 取得所有的分类
     return redirect( 'article_list')#这里的隐射返回跳转的地址，可以是name=’article_list’来拿也可以是匹配前面的正则来那地址
     # res= models.article.objects.all()#删除后再次查找数据库内容
     # return render(request,'myadmin/article_list',{'res':res})#把查到的参数，数据，跳转到列表页然后用参数渲染后返回

#--------------文章end-------------------


#--------------网站配置start--------------------
def config(request):
    if request.method =='GET':
        count=models.config.objects.all().count()
        if not count:
             #由于我config表中其他字段都可以为空，所以只给id赋值
            models.config.objects.create(id=1)
        res=models.config.objects.get(id=1)
        return render(request,'myadmin/config.html',{'res':res})
    else:
        data={}
        id=request.POST.get('id')
        data['title']=request.POST.get('title')
        data['keywords'] = request.POST.get('keywords')
        data['description'] = request.POST.get('description')
        data['about_us'] = request.POST.get('about_us')
        data['connect_us'] = request.POST.get('connect_us')
        logo=request.FILES.get('logo')
        #判断是否上传图片
        if logo:
            #取得原图片名
            img_name=logo.name
            #取得图片后缀
            img_type=img_name.split('.')[-1]
            #图片新名字
            new_img_name='logo.'+img_type
            #存储路径
            image_addr='static/'+ new_img_name
            with open(image_addr,'wb') as f:
                f.write(logo.read())
                #将图片地址赋值给添加的图片字段

            data['logo']='/'+ image_addr
                #修改操作
        models.config.objects.filter(id=id).update(**data)
        return redirect('/myadmin/config')



#--------------网站配置end------------------------


#—————————————留言开始————————
#分类列表
@check_cookie
def message_list(request):#定义分类列表函数
    # 取得当前页数
    cur_page = int(request.GET.get('p', 1))  # 第一次展示列表页数数据时没有p参数默认是1
    NUM = 3  # 每页显示的会员信息数据条数，可设置
    COUNT = models.message.objects.count()  # 总的会员信息记录条数

    page = math.ceil(COUNT / NUM)  # 调用math.ceil()函数来计算出需要显示的所有总页数
    print(page)
    # 页数的样式
    page_html = ''  # 空字符串
    for i in range(1, page + 1):
        # 当前页
        if i == cur_page:
            page_html += '<a class="curpage" href="/myadmin/message_list?p=%d">%d</a>' % ( i, i)  # 如果当前页和请求一致。显示的页数为样式设置的颜色
        else:
            page_html += '<a href="/myadmin/message_list?p=%d">%d</a>' % (i, i)  # 否则显示的页数没有加样式
    res = models.message.objects.all().order_by('-id')[(cur_page - 1) * 3:cur_page * 3]  # 读取所有列表信息，并倒序排序
    return render(request, 'myadmin/message_list.html', {'res': res, 'page_html': page_html})


#添加分类列表
@csrf_exempt
def message_add(request):
    #取得参数
    name=request.POST.get('my_name')
    #插入到article数据库中
    models.message.objects.create(my_name=name)
    return redirect('/myadmin/message_list')
#删除分类操作
@check_cookie
def message_del(request):

    id=request.GET.get('id')
    #数据库操作
    models.message.objects.filter(id=id).delete()

    #页面重定向
    return redirect('/myadmin/message_list')

#修改分类操作
@check_cookie
def message_edit(request):
    id=request.GET.get('id')

    content=request.GET.get('content')
    models.message.objects.filter(id=id).update(content=content)
    return HttpResponse('操作成功')

#——————-文章分类end————————



















