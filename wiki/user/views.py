import datetime
import hashlib
import json
import time

import jwt
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from user.weiboapi import OAuthWeibo
from .models import UserProfile,WeiboUser
from wtoken.views import make_token
from tools.logging_check import logging_check


# Create your views here.


@logging_check('PUT')
def users(request, username=None):

    if request.method == 'GET':
        if username:
            users = UserProfile.objects.filter(username=username)
            user = users[0]
            #TODO 没用户 返回提示
            #拿具体用户数据
            #有查询字符串[?nickname=1] or 没查询字符串
            if request.GET.keys():
                #查询字符串
                data = {}
                for k in request.GET.keys():
                    if hasattr(user, k):
                        #过滤字段
                        if k == 'password':
                            continue
                        v = getattr(user, k)
                        data[k] = v
                res = {'code':200, 'username':username, 'data':data}

            else:
                #无查询字符串
                res = {'code':200, 'username':username,'data':{'nickname':user.nickname,'sign':user.sign,'info':user.info,'avatar':str(user.avatar)}}

            return JsonResponse(res)
        else:
            #拿数据
            all_users = UserProfile.objects.all()
            users_data = []
            for user in all_users:
                dic = {}
                dic['nickname'] = user.nickname
                dic['username'] = user.username
                dic['sign'] = user.sign
                dic['info'] = user.info
                users_data.append(dic)
            res = {'code':200, 'data':users_data}
            return JsonResponse(res)

    elif request.method == 'POST':
        #创建用户
        json_str = request.body
        if not json_str:
            result = {'code':10102, 'error':'Please give me data~'}
            return JsonResponse(result)

        json_obj = json.loads(json_str)
        username = json_obj.get('username')
        email = json_obj.get('email')
        if not username:
            result = {'code':10101, 'error':'Please give me username~'}
            return JsonResponse(result)
        #TODO 检查 json dict 中的key 是否存在
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        if password_1 != password_2:
            result = {'code': 10103, 'error':'The password is error!' }
            return JsonResponse(result)

        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10104, 'error':'The username is already existed !'}
            return JsonResponse(result)

        #生成散列密码
        pm = hashlib.md5()
        pm.update(password_1.encode())

        wuid = json_obj.get('wuid')


        #创建用户
        try:
            with transaction.atomic():

                new_user = UserProfile.objects.create(username=username, password=pm.hexdigest(),nickname=username,email=email)
                if wuid:
                    w_obj = WeiboUser.objects.get(wuid=wuid)
                    #绑定微薄用户和博客用户
                    w_obj.buser = new_user
                    w_obj.save()

        except Exception as e:
            print('---create error---')
            print(e)
            result = {'code':10105, 'error':'The username is already existed !!'}
            return JsonResponse(result)

        #生成token
        now = datetime.datetime.now()
        token = make_token(username, 3600*24, now)
        result = {'code':200, 'data':{'token':token.decode()},'username':username}
        return JsonResponse(result)


    elif request.method == 'PUT':
        #更新  http://127.0.0.1:8000/v1/users/username
        if not username:
            res = {'code':10108, 'error':'Must be give me username !!'}
            return JsonResponse(res)



        json_str = request.body
        #TODO 空Body判断
        json_obj = json.loads(json_str)
        nickname = json_obj.get('nickname')
        sign = json_obj.get('sign')
        info = json_obj.get('info')
        #更新
        # users = UserProfile.objects.filter(username=username)
        # user = users[0]

        user = request.user
        #当前请求，token用户 修改自己的数据
        if user.username != username:
            result = {'code': 10109, 'error':'The username is error !'}
            return JsonResponse(result)

        to_update = False
        if user.nickname != nickname:
            to_update = True
        if user.info != info:
            to_update = True
        if user.sign != sign:
            to_update = True

        if to_update:
            #做更新
            user.sign = sign
            user.nickname = nickname
            user.info = info
            user.save()
        return JsonResponse({'code':200, 'username':username})



@logging_check('POST')
def users_avatar(request, username):
    #处理头像上传
    if request.method != 'POST':
        result = {'code': 10110, 'error': 'Please use POST'}
        return JsonResponse(result)
    user = request.user
    if user.username != username:
        result = {'code': 10109, 'error': 'The username is error !'}
        return JsonResponse(result)

    user.avatar = request.FILES['avatar']
    user.save()
    return JsonResponse({'code':200, 'username':username})

def users_weibo_url(request):

    oauth = OAuthWeibo('123')
    oauth_weibo_url = oauth.get_weibo_login()
    return JsonResponse({'code':200, 'oauth_url': oauth_weibo_url})


def users_weibo_token(request):
    #接收 前端返回的code 并 去微博校验
    code = request.GET.get('code')
    oauth = OAuthWeibo()
    #向微博服务器提交code,若校验成功 返回该用户的token
    res = oauth.get_access_token_uid(code)
    res_obj = json.loads(res)
    access_token = res_obj['access_token']
    uid = res_obj['uid']

    #检查当前这个用户是否注册过我们博客
    try:
        bu = WeiboUser.objects.get(wuid=uid)
    except:
        #用户第一次 用微博账号登录
        #TODO?
        WeiboUser.objects.create(wuid=uid,access_token=access_token)
        return JsonResponse({'code':10999, 'wuid':uid})
    else:
        #检查是否真的绑定过
        buser = bu.buser
        if not buser:
            return JsonResponse({'code': 10999, 'wuid': uid})
        now = datetime.datetime.now()
        token = make_token(buser.username, 3600*24, now)
        return JsonResponse({'code':200, 'username':buser.username, 'data':{'token':token.decode()}})


































