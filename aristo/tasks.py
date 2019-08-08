from __future__ import absolute_import, unicode_literals
from celery import shared_task,app,task
import time
from .models import Instagram_Accounts_Analyse,IG_Users,Analyse_FF
from Instagram_api import private_api
from django_celery_results.models import TaskResult


@shared_task
def user_details(i,username,password):
    print(i,username,password)
    #celery_task = TaskResult.objects.get(task_id=self.request.id)
    #run=Run(task=celery_task)
    #run.save()

    api=private_api.login_instagram(username,password)
    try:
        user_detail = IG_Users.objects.filter(pk_number=i)[0]
    except:
        info = private_api.get_user_info(i,api)
        #kullanıcı hesabı analiz sırasında silerse patlayabilir. 
        user_detail = IG_Users(full_name=info[0],
                            pk_number=info[1],
                            profile_pic_url=info[5],is_hidden=info[6],
                            number_of_followers=info[7], is_business=info[8],
                            biography=info[9], number_of_medias=info[10],
                            number_of_followings=info[11],username=info[13])

        user_detail.save()
    
    friendship=private_api.show_friendship_status(i,api)
    following=friendship[0]
    followed_by=friendship[1]
    ig_account_analyse=Instagram_Accounts_Analyse.objects.filter(instagram_account__username=username)[0]
    Analyse=Analyse_FF(instagram_account_analyse=ig_account_analyse,ig_user_details=user_detail,is_following=following,is_follower=followed_by)
    Analyse.save()

         

