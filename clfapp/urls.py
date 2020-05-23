from django.urls import path
from . import views

app_name = 'clfapp'

urlpatterns = [
    path(route='', view=views.index, name='index'),
    path(route='login/', view=views.login, name='login'),
    path(route='get_text/', view=views.get_text, name='get_text'),
    path(route='uploadfile/', view=views.uploadfile, name='upfile'),

    # 测试文件上传时使用
    # path(route='model_form_upload/', view=views.model_form_upload, name='model_form_upload'),
    # path(route='simple_upload/', view=views.simple_upload, name='simple_upload'),

    # 匹配的路由为''，使用的视图函数为view.py下的index(),在其他地方引用该url时，使用index
    # path('', views.login, name='login'),
    # path('login/', views.login, name='login'),
    # path('get_text/', views.get_text, name='get_text'),

]
