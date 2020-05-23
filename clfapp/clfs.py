import codecs
import csv
import os

import pandas as pd
import numpy as np
import jieba
import joblib
# django package
from django.conf import settings

# import from.py
from .models import Settings, Models, Uploadfile

# 引入mdeia_root参数
media_path = settings.MEDIA_ROOT


# filepath = os.path.join(settings.MEDIA_ROOT, 'name.txt')

def list_to_csv(list1, list2, filepath,):
    list = [list1, list2]
    array = np.asarray(list)
    array = array.T
    # print(array)
    col_name = ['mails', 'categories(1:spam;0:ham)']
    test = pd.DataFrame(columns=col_name, data=array)
    test.to_csv(filepath, encoding='gbk')


# 调用jieba分词,返回值为一个将分词结果为：list('word1 word2 word3')
def jiebacut(text):
    b = list()
    cut_result = jieba.lcut(text)
    b.append(' '.join(cut_result))
    return b


# 接收uid和分词结果（形如list('word1 word2 word3','word4 word5 word6')），返回结果为[1,1,0...,1]的形式
def classify(uid, word_cut_result):
    # 数据库查询配置
    setting = Settings.objects.get(user_id=uid)
    # 确认模型存储路径
    vec_path = Models.objects.get(model_name__exact=setting.vec_id).model_upload
    clf_path = Models.objects.get(model_name__exact=setting.clf_id).model_upload
    # 装载模型
    tmp_vec = joblib.load(os.path.join(media_path, str(vec_path)))
    tmp_clf = joblib.load(os.path.join(media_path, str(clf_path)))

    # 开始判断邮件种类
    vectorize = tmp_vec.transform(word_cut_result)
    # tmp_clf.predict(vectorize) 是一个array形式的数据，将其转化为list
    result = list(tmp_clf.predict(vectorize))
    # flag-1
    # print(result)
    # 返回分词的list
    return result

# 单挑处理
def handle_single(uid, mail):
    word_cut = list()
    word_cut.append(' '.join(jieba.lcut(mail)))
    # print(word_cut)
    # print(classify(uid, word_cut))
    # return 0
    return classify(uid, word_cut)[0]



# 批量处理
def handle_uploaded_file(uid):
    # id表示按照user_id的升序排序，- 表示按照降序，[:1]表示取最后一个

    filepath_db = str(Uploadfile.objects.filter(user_id=uid).order_by('-id')[:1].get().file)
    filepath = os.path.join(settings.MEDIA_ROOT, filepath_db)
    # print(filepath)
    f = open(filepath, 'r', encoding='utf-8')
    word_cut_result = list()
    mail_list = list()
    for line in f.readlines():
        line = line.strip()
        mail_list.append(line)
        word_cut_result.append(' '.join(jieba.lcut(line)))
    result_list = classify(uid, word_cut_result)
    # 邮件list和结果list准备完毕，开始写入文件，函数返回值为其url
    # filepath文件夹名
    # filename不带后缀文件名
    # extension后缀名
    (path_db, tempfilename) = os.path.split(filepath_db)
    (filename, extension) = os.path.splitext(tempfilename)

    new_file_name = filename + '_Done'+'.csv'
    # django内部路径
    new_file_path = os.path.join(path_db, new_file_name)
    print(new_file_path)
    # 保存文件的系统路径
    path_for_save = os.path.join(settings.MEDIA_ROOT, new_file_path)
    print(path_for_save)
    # flag-2
    # print(mail_list, result_list)
    list_to_csv(mail_list, result_list, path_for_save)

    return new_file_path


