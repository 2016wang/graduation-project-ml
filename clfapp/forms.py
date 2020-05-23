from django import forms

# from .models import Upfiles
# from .models import Document
from .models import Uploadfile


class UploadfileForm(forms.ModelForm):

    class Meta:
        model = Uploadfile
        exclude = ['user_id']
        labels = {
            "file": ""
        }
        widgets = {
            "file": forms.widgets.FileInput(attrs={"class": "custom-file-input"}),
        }




class mailForm(forms.Form):
    your_mail = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'rows': "3"}),
        label='输入待分类邮件内容',
        max_length=300,
    )


class loginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs=
        {
            'class': "form-control",
            'placeholder': 'Username',
        }
            ),
        label='',
        max_length=30,
    )


# 测试时使用，用于简单的上传
'''
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
'''

# 测试时使用，用的ModelForm上传
'''
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
'''
