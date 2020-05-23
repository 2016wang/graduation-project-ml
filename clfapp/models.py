from django.db import models


# Create your models here.


class Users(models.Model):
    uid = models.AutoField('user id', primary_key=True)
    username = models.CharField('user name', max_length=30, unique=True)

    def __str__(self):
        return self.username


'''def filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<filename>
    return '{0}'.format(filename)'''


class Models(models.Model):
    mid = models.AutoField('model id', primary_key=True)
    model_name = models.CharField('model name', max_length=30, unique=True)
    model_upload = models.FileField('upload models', upload_to='models/')
    model_desc = models.CharField('model desc', max_length=100)

    def __str__(self):
        return self.model_name


class Settings(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    word_cut_id = models.IntegerField('word cut id')
    vec_id = models.ForeignKey(Models, related_name='vectorizer', on_delete=models.CASCADE)
    clf_id = models.ForeignKey(Models, related_name='classficer', on_delete=models.CASCADE)

    def __str__(self):
        return "{0}的配置".format(Users.objects.get(uid=self.id).username)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_id/<filename>
    # 不同的用户放在不同的文件中
    '''print(type(instance))
    print(instance.user_id)
    print(instance.user_id.uid)
    print(instance.description)'''
    # 利用uid新建文件
    return 'upfiles/user_{0}/{1}'.format(instance.user_id.uid, filename)


class Uploadfile(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# 用来测试
'''
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    # document = models.FileField(upload_to='upfiles/')
    document = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
'''
