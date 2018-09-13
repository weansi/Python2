"""myloog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls import url
from myadmin import views as admin_views
from home import views
from myadmin.uploads import upload_image
urlpatterns = [
    #path('admin/', admin.site.urls),
    #home 前端路由匹配

    url(r'^$',views.index,name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^article$', views.article, name='article'),
    # url(r'^caselist$',views.caselist,name='caselist'),
     url(r'^article1$',views.article1,name='article1'),
     url(r'^tianjin$', views.tianjin, name='tianjin'),
     url(r'^article2$', views.article2, name='article2'),
     url(r'^beijing$', views.beijing, name='beijing'),
     url(r'^article3$', views.article3, name='article3'),
     url(r'^shanghai$', views.shanghai, name='shanghai'),
    # url(r'^knowledge$',views.knowledge,name='knowledge'),
    # url(r'^moodlist$',views.moodlist,name='moodlist'),
    # url(r'^new$', views.new, name='new'),

    # url(r'^newlist$', views.newlist, name='newlist'),
    # url(r'^template$', views.template, name='template'),

     # url(r'^article1$', views.article1, name='article1'),

     # url(r'^home/get_code$', views.get_code, name='get_code'),
     # url(r'^home/cat_name$', views.cat_name, name='cat_name'),



# #留言板匹配
   url(r'^message$',views.message, name='message'),
   url(r'^newlist$',views.newlist, name='newlist'),
   url(r'^get_code$', admin_views.get_code, name='get_code'),



    #后台路由匹配
    url(r'^myadmin/$',admin_views.index),
    url(r'^myadmin/login$',admin_views.login,name='login'),#登陆路由
    url(r'^myadmin/check_login$', admin_views.check_login, name='check_login'),  # 登陆ajax验证
    url(r'^myadmin/login_out$', admin_views.login_out, name='login_out'),
    url(r'^myadmin/check_code$', admin_views.check_code, name='check_code'),
    url(r'^myadmin/get_code$', admin_views.get_code, name='get_code'),
    url(r'^myadmin/check_user$', admin_views.check_user, name='check_user'),

    url(r'^myadmin/admin_list$',admin_views.admin_list,name='admin_list'),
    url(r'^myadmin/admin_add$', admin_views.admin_add,name='admin_add'),
    url(r'^myadmin/admin_del$', admin_views.admin_del, name='admin_del'),
    url(r'^myadmin/admin_edit$', admin_views.admin_edit, name='admin_edit'),

   #文章分类匹配
    url(r'^myadmin/article_cat_list$', admin_views.article_cat_list, name='article_cat_list'),
    url(r'^myadmin/article_cat_add$', admin_views.article_cat_add, name='article_cat_add'),
    url(r'^myadmin/article_cat_edit$', admin_views.article_cat_edit, name='article_cat_edit'),
    url(r'^myadmin/article_cat_del$', admin_views.article_cat_del, name='article_cat_del'),
#文章匹配
    url(r'^myadmin/article_list$', admin_views.article_list, name='article_list'),
    url(r'^myadmin/article_add$', admin_views.article_add, name='article_add'),
    url(r'^myadmin/article_edit$', admin_views.article_edit, name='article_edit'),
    url(r'^myadmin/article_del$', admin_views.article_del, name='article_del'),

 # 网站配置：
    url(r'^myadmin/config$', admin_views.config, name='config'),

    # 富文本编辑器图片上传路由
    url(r'^upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),

    #留言匹配
    url(r'^myadmin/message_list$', admin_views.message_list, name='message_list'),
    url(r'^myadmin/message_edit$', admin_views.message_edit, name='message_edit'),
    url(r'^myadmin/message_add$', admin_views.message_add, name='message_add'),
    url(r'^myadmin/message_del$', admin_views.message_del, name='message_del'),
]
