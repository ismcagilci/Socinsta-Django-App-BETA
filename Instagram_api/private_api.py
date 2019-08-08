import json
import codecs
import datetime
import os.path
import logging
import argparse
from aristo.models import *
from aristo.tasks import user_details

import ssl


ssl._create_default_https_context = ssl._create_unverified_context


from django.contrib.auth.models import User
try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object[ '__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object



def check_is_real(username,password):
    try:
        api=Client(username,password)
        return True
    except Exception as e:
        print(e)
        return False


def create_cookie(cache_settings,username):
    #Eski onlogin_callback fonksiyonu. Cookie yoksa onu kaydediyor sadece. O yüzden ismini değiştirdim.
    insta_user=Instagram_Accounts.objects.get(username=username)
    cookie=cache_settings.get("cookie")
    cache_settings.__delitem__("cookie")
    json_settings=json.dumps(cache_settings)
    new_settings=Api_Settings(instagram_account=insta_user,cookie=cookie,settings=json_settings)
    new_settings.save()

def login_instagram(username,password):
    device_id = None
    api_settings = Api_Settings.objects.filter(instagram_account__username=username)
    try:
        if len(api_settings)==0:       
            print("yeni_ayar")
            api = Client(username, password)
            create_cookie(api.settings,username)
            
        else:
            settings=api_settings[0].settings
            cookie=api_settings[0].cookie
            settings=json.loads(settings)
            settings["cookie"]=cookie
            device_id = settings.get('device_id')
            print("ayarlar_kullanılıyor")
            api = Client(
                    username, password,
                    settings=settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        Api_Settings.objects.filter(instagram_account__username=username).delete()
        api = Client(   username, password,device_id=device_id)
        create_cookie(api,username)

    return api

def get_user_cookie(api):
    cookie=api.settings
    return cookie

def ranktoken():
    rank_token = Client.generate_uuid()
    return rank_token

def get_user_pk(username,api):
    info=api.username_info(username)
    pk=info.get("user").get("pk")
    return pk

def get_user_info(user_pk,api):
    user_info_dict_all=api.user_info(user_pk)
    user_info_dict=user_info_dict_all.get("user")
    liste=[]
    username = user_info_dict.get("username")
    full_name = user_info_dict.get("full_name")
    pk = user_info_dict.get("pk")
    is_verified=user_info_dict.get("is_verified")
    external_url=user_info_dict.get("external_url")
    has_anonymous_profile_picture=user_info_dict.get("has_anonymous_profile_picture")
    if has_anonymous_profile_picture==False:
        has_anonymous_profile_picture=0
    else:
        has_anonymous_profile_picture=1
    profile_pic_url=user_info_dict.get("profile_pic_url")
    is_private=user_info_dict.get("is_private")
    if is_private==False:
        is_private=0
    else:
        is_private=1
    follower_count=user_info_dict.get("follower_count")
    is_business=user_info_dict.get("is_business")
    if is_business==False:
        is_business=0
    else:
        is_business=1
    biography=user_info_dict.get("biography")
    if len(biography)!=0:
        biography=1
    else:
        biography=0
    media_count=user_info_dict.get("media_count")
    following_count=user_info_dict.get("following_count")
    usertags_count=user_info_dict.get("usertags_count")
    liste.append((full_name,pk,is_verified,external_url,has_anonymous_profile_picture,profile_pic_url,is_private,follower_count,is_business
                  ,biography,media_count,following_count,usertags_count,username))
    return liste[0]


def get_like_count(username,api):
    user_pk=get_user_pk(username,api)
    like_count=0
    feeds=api.user_feed(user_pk)
    for i in feeds.get("items"):
        like_count+=i.get("like_count")
    return like_count

def get_comment_count(username,api):
    user_pk=get_user_pk(username,api)
    comment_count=0
    feeds=api.user_feed(user_pk)
    for i in feeds.get("items"):
        comment_count+=i.get("comment_count")
    return comment_count

def get_post_count(username,api):
    user_pk=get_user_pk(username,api)
    post_count=0
    feeds=api.user_feed(user_pk)
    post_count+=len(feeds.get("items"))
    return post_count

def show_friendship_status(user_pk,api):
    status=api.friendships_show(user_pk)
    status_list=[]
    status_list.append(status.get("following"))
    status_list.append(status.get("followed_by"))
    for i in status_list:
        if i==False:
            i=1
        else:
            i=0
    return status_list

def get_user_followers(username,api):
    user_pk=get_user_pk(username,api)
    rank_token=api.generate_uuid()
    liste=[]
    next_max_id=api.user_followers(user_pk,rank_token).get("next_max_id")
    followers=api.user_followers(user_pk,rank_token).get("users")
    for i in followers:
        liste.append(i.get("pk"))
    while next_max_id:
        followers = api.user_followers(user_pk, rank_token,max_id=next_max_id).get("users")
        next_max_id = followers.get("next_max_id")
        for i in followers:
            liste.append(i.get("pk"))
    return liste

def get_user_followings(username,api):
    user_pk=get_user_pk(username,api)
    rank_token=api.generate_uuid()
    liste=[]
    next_max_id=api.user_following(user_pk,rank_token).get("next_max_id")
    followings=api.user_following(user_pk,rank_token).get("users")
    for i in followings:
        liste.append(i.get("pk"))
    while next_max_id:
        followings = api.user_following(user_pk, rank_token,max_id=next_max_id).get("users")
        next_max_id = followings.get("next_max_id")
        for i in followings:
            liste.append(i.get("pk"))
    print('!!!!!!!!!!!!!!',liste, '!!!!!!!!!!!!!!')
    return liste


def get_analysis(IG_Account): 
 
    username = IG_Account.username
    password = IG_Account.password
    api = login_instagram(username,password)

    #IG Analiz Objesi oluşturuyor.
    like_count = get_like_count(username,api)
    comment_count = get_comment_count(username,api)
    post_count = get_post_count(username,api)
    ig_account_analysis = Instagram_Accounts_Analyse(instagram_account=IG_Account,like_count=like_count,post_count=post_count,comment_count=comment_count)
    ig_account_analysis.save()

    #Takipçi ve takip edilenlerin detaylı analizi ekleniyor.

    user_followers=get_user_followers(username,api)
    user_followings=get_user_followings(username,api)
    analyse_list = set(user_followers+user_followings)

    #Celery Kısmı
    for i in analyse_list:   
        user_details.delay(i,username,password)
    #Add_insta_account viewine info dönüyor.
    pk=get_user_pk(username,api)
    info=get_user_info(pk,api)

    return info

