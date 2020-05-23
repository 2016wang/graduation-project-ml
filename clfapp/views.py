# request and response
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# import clf.py
from .clfs import handle_uploaded_file, handle_single
from .clfs import classify
# import form.py
# from .forms import UploadFileForm, DocumentForm, UpfilesForm
from .forms import UploadfileForm, loginForm, mailForm
# import model.py
from .models import Uploadfile, Users


# 用来做导航
def index(request):
    return render(request, 'clfapp/index.html',)


# 查询用户名并确认用户身份
def is_valid_user(username):
    try:
        Users.objects.get(username=username)
        return True
    except ObjectDoesNotExist:
        return False

    # #调用模型进行单个邮件判定


# 用户认证
def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            is_valid = is_valid_user(username)
            if is_valid:
                request.session['islogin'] = True
                uid = Users.objects.get(username=username).uid
                request.session['uid'] = uid
                request.session.set_expiry(3600)
                return redirect('clfapp:index')
            else:
                err = '该用户不存在'
                form = loginForm()
                return render(request, 'clfapp/login.html', {'form': form, 'err': err})
    else:
        form = loginForm()
        return render(request, 'clfapp/login.html', {'form': form})

# 通过测试该def，发现返回的request.POST是QueryDict格式，可以用get直接获取。

# 用户上传单条信息
def get_text(request):
    if request.session.get('islogin', False):
    # if True:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = mailForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                mail = form.cleaned_data['your_mail']
                print(mail)
                uid = request.session.get('uid')
                # 调用分类模块
                result = handle_single(uid, mail)
                if result:
                    result = '垃圾邮件'
                else:
                    result = '正常邮件'
                # redirect to a new URL:
                # 新建一个form对象
                form = mailForm()
                return render(request, "clfapp/input.html", {'form': form, 'result': result})
                # return HttpResponseRedirect('/thanks/')
                # return HttpResponse(result)
        # if a GET (or any other method) we'll create a blank form
        else:
            form = mailForm()
            result = None
            return render(request, "clfapp/input.html", {'form': form, 'result': result})
    else:
        form = loginForm()
        return render(request, 'clfapp/login.html', {'form': form})

'''
def uploadfile(request):
    if request.session.get('islogin', False):

        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            # 上传的同时能够获取上传文件的位置，方便直接访问。
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            return render(request, 'clfapp/simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })
        return render(request, 'clfapp/simple_upload.html')
'''

def uploadfile(request):
    if request.session.get('islogin', False):
    # if True:
        file_path = None
        if request.method == 'POST' and request.FILES['file']:
            #通过uid实例化一个Users
            form = UploadfileForm(request.POST, request.FILES)
            if form.is_valid():
                # 测试FILES函数
                # print(request.FILES['file'].name)
                # print(request.FILES['file'].size)
                # print(request.FILES['file'].content_type)
                # print(request.FILES['file'].content_type_extra)
                # print(request.FILES['file'].charset)
                # print(request.FILES['file'].chunks)
                
                uid = request.session.get('uid')
                # 可以正常运行了。
                ### 存入数据库
                upfile = form.save(commit=False)
                upfile.user_id = Users.objects.get(uid=uid)
                upfile.save()
                ### 原始文件上传结束

                # 执行分类操作，并返回分类结果
                file_path = handle_uploaded_file(uid)
                print(file_path)

                form = UploadfileForm()
                return render(request, 'clfapp/uploadfile.html', {'form': form, 'file_path': file_path})

            # 下一步转化为 文件列表
        else:
            form = UploadfileForm()
            return render(request, 'clfapp/uploadfile.html', {'form': form, 'file_path': file_path},)
    else:
        return redirect('/clfapp/login')



'''
author = Author(title='Mr')
form = PartialAuthorForm(request.POST, instance=author)
form.save()
或
form = PartialAuthorForm(request.POST)
author = form.save(commit=False)
author.title = 'Mr'
author.save()
#验证文件不为空
form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
或
request.File['file'] 不为 None
'''

# 保留该容错示例，是为了更好的实现代码的容错机制。try except else
'''def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))'''

# 该方法示例————如何完成简单的上传——借助django中的FileSystemStorage工具。
'''
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        # 上传的同时能够获取上传文件的位置，方便直接访问。
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        return render(request, 'clfapp/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'clfapp/simple_upload.html')
'''

# 该示例演示ModelForm如何运行。
'''
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form)
            # form.save()
            return redirect('clfapp:index')
    else:
        form = DocumentForm()
    return render(request, 'clfapp/model_form_upload.html', {
        'form': form
    })
'''
