
from django.db import models
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult


# Create your models here.


class Run(models.Model):
    task = models.ForeignKey(TaskResult, on_delete=models.DO_NOTHING)

class Licanse(models.Model):
    main_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type_of_licanse = models.CharField(max_length=200, verbose_name="Type of Licanse", null=True)
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Register Date")
    def __str__(self):
        return self.type_of_licanse



class Instagram_Accounts(models.Model):
    main_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=200, verbose_name="username", null=True)
    password= models.CharField(max_length=200, verbose_name="password", null=True)
    is_current_account=models.IntegerField(verbose_name="is current account",null=True)

    def __str__(self):
        return self.username

    

class Assistants(models.Model):
    instagram_account = models.ForeignKey(Instagram_Accounts,on_delete=models.CASCADE,null=True)
    assistant_action_type = models.IntegerField(verbose_name='Assistant_action_type',null=True)
    assistant_source_type = models.IntegerField(verbose_name="Assistant_source_type",null=True)
    number_of_actions = models.IntegerField(verbose_name='number_of_actions',null=True)
    
    def __str__(self):
        return str(self.instagram_account)


class Assistants_Settings(models.Model):
    min_followers = models.IntegerField(verbose_name='min_followers',null=True)
    max_followers = models.IntegerField(verbose_name='max_followers',null=True)
    min_followings = models.IntegerField(verbose_name='min_followings',null=True)
    max_followings = models.IntegerField(verbose_name='max_followings',null=True)
    min_posts = models.IntegerField(verbose_name='min_posts',null=True)
    max_posts = models.IntegerField(verbose_name='max_posts',null=True)
    biography = models.IntegerField(verbose_name='biography',null=True)
    is_hidden = models.IntegerField(verbose_name='hidden_account',null=True)
    is_business = models.IntegerField(verbose_name='is_bussines',null=True)
    assistant=models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.assistant.instagram_account.username




class IG_Users(models.Model):
    username = models.CharField(max_length=200, verbose_name="username", null=True)
    full_name = models.CharField(max_length=200, verbose_name="full_name", null=True)
    pk_number = models.IntegerField(verbose_name='pk_number', null=True)
    profile_pic_url = models.CharField(max_length=300, verbose_name="profile_pic_url", null=True)
    number_of_followers = models.IntegerField(verbose_name='number_of_followers', null=True)
    number_of_followings = models.IntegerField(verbose_name='number_of_followings', null=True)
    biography = models.IntegerField(verbose_name='biography', null=True)
    is_business = models.IntegerField(verbose_name='is_business', null=True)
    is_hidden = models.IntegerField(verbose_name='is_hidden', null=True)
    number_of_medias = models.IntegerField(verbose_name='number_of_medias', null=True)

    def __str__(self):
        return self.username

class Instagram_Accounts_Analyse(models.Model):
    instagram_account=models.ForeignKey(Instagram_Accounts,on_delete=models.CASCADE,null=True)
    like_count=models.IntegerField(verbose_name="like_count",null=True)
    post_count=models.IntegerField(verbose_name="post_count",null=True)
    comment_count=models.IntegerField(verbose_name="comment_count",null=True)
    update_time = models.DateTimeField(auto_now_add=True,verbose_name="update_time",null=True)

    def __str__(self):
        return self.instagram_account.username        

class Analyse_FF(models.Model):
    instagram_account_analyse=models.ForeignKey(Instagram_Accounts_Analyse,on_delete=models.CASCADE,null=True)
    ig_user_details=models.ForeignKey(IG_Users,on_delete=models.CASCADE,null=True)
    is_following=models.IntegerField(verbose_name="is_following",null=True)
    is_follower=models.IntegerField(verbose_name="is_follower",null=True)
    def __str__(self):
        return self.instagram_account_analyse.instagram_account.username


class Follow_Actions(models.Model):
    assistant = models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True)
    ig_user = models.ForeignKey(IG_Users,on_delete=models.CASCADE,null=True)
    status = models.IntegerField(verbose_name='status', null=True)
    update_time = models.DateTimeField(auto_now_add=True,verbose_name="update_time",null=True)

    def __str__(self):
        return str(self.assistant)


class IG_Posts(models.Model):
    post_id=models.IntegerField(verbose_name="post_id", null=True)
    post_user=models.CharField(max_length=200, verbose_name="post_user",null=True)

    def __str__(self):
        return str(self.post_id)

class Like_Actions(models.Model):
    assistant = models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True)
    ig_post = models.ForeignKey(IG_Posts,on_delete=models.CASCADE,null=True)
    status = models.IntegerField(verbose_name='status', null=True)
    update_time = models.DateTimeField(auto_now_add=True,verbose_name="update_time",null=True)

    def __str__(self):
        return str(self.assistant)

class Comment_Actions(models.Model):
    assistant = models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True)
    ig_post = models.ForeignKey(IG_Posts,on_delete=models.CASCADE,null=True)
    comment = models.CharField(max_length=200, verbose_name="comment",null=True)
    status = models.IntegerField(verbose_name='status', null=True)
    update_time = models.DateTimeField(auto_now_add=True,verbose_name="update_time",null=True)

    def __str__(self):
        return str(self.assistant)

class Assistant_User(models.Model):
    username = models.CharField(max_length=200,verbose_name="Username",null=True)
    own=models.IntegerField(verbose_name="Own",null=True)
    followers = models.IntegerField(verbose_name="Followers",null=True)
    followings = models.IntegerField(verbose_name="Followings",null=True)
    likers = models.IntegerField(verbose_name="Likers",null=True)
    commenters = models.IntegerField(verbose_name="Commenters",null=True)
    assistant=models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.assistant)

class Assistant_Hashtag(models.Model):
    hashtag = models.CharField(max_length=200,verbose_name="Hashtag",null=True)
    posters = models.IntegerField(verbose_name="Posters",null=True)
    likers = models.IntegerField(verbose_name="Likers",null=True)
    commenters = models.IntegerField(verbose_name="Commenters",null=True)
    assistant=models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.assistant)

class Assistant_Location(models.Model):
    location = models.CharField(max_length=200,verbose_name="Location",null=True)
    posters = models.IntegerField(verbose_name="Posters",null=True)
    likers = models.IntegerField(verbose_name="Likers",null=True)
    commenters = models.IntegerField(verbose_name="Commenters",null=True)
    assistant=models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.assistant)


class Api_Settings(models.Model):
    instagram_account=models.ForeignKey(Instagram_Accounts,on_delete=models.CASCADE,null=True)
    update_time = models.DateTimeField(auto_now_add=True,verbose_name="update_time",null=True)
    cookie=models.BinaryField(verbose_name="binary",null=True)
    settings=models.TextField(verbose_name="settings",null=True)
    def __str__(self):
        return self.instagram_account.username


















