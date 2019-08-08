from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from Instagram_api import private_api
import time
from .tasks import *

# Create your views here.

def login_user(request):
    if request.POST:
        username=request.POST["site_username"]
        password=request.POST["site_password"]
        control_user=User.objects.filter(username = username)
        if len(control_user)==0:
            return render(request,"login.html",{"x":"block","y":"Böyle bir kullanıcı bulunamadı!"})
        else:
            user = authenticate(username=username, password=password)
            login(request,user)
            return render(request,"profile.html",{"wow":"none","wow2":"block","confirmation_message":"confirmation_message2()"})

    return render(request,"login.html",{"x":"none"})

def register(request):
    if request.POST:
        username=request.POST["site_username"]
        email=request.POST["site_email"]
        password=request.POST["site_password"]
        password_again=request.POST["site_password_again"]
        if len(username)==0 or len(email)==0 or len(password)==0 or len(password_again)==0:
            return render(request,"register.html",{"x":"block","y ":"Lütfen boş yerleri doldurun"})
        
        if password != password_again:
            return render(request,"register.html",{"x":"block","y":"Parolalar eşleşmiyor"})
        
        control_user=User.objects.filter(username = username)
        try:
            if len(control_user)==0:
                newUser=User(username=username,email=email)
                newUser.set_password(password)
                newUser.save()
                login(request,newUser)

                #print(request.user)

                return render(request,"profile.html",{"wow":"none","wow2":"block","confirmation_message":"confirmation_message()"})
            else:
                return render(request,"register.html",{"x":"block","y":"Hesap zaten kayıtlı!"})
        except:
            return render(request,"register.html",{"x":"block","y":"Hesap zaten kayıtlı"})
    else:
        return render(request,"register.html",{"x":"none"})

def landing(request):
    return render(request, "landing.html")

def pricing(request):
    return render(request,"pricing.html")


def logout_user(request):
    logout(request)
    return render(request,"landing.html",{"confirmation_message":"confirmation_message()"})



#Dashboard Views


# Create your views here.


def dashboard(request):

    if len(Instagram_Accounts.objects.filter(is_current_account=1))==0:
        return render(request, "profile.html")


    return render(request, "dashboard.html",{"deneme":3})

def add_insta_account(request):
    if request.POST:
        username=request.POST["instagram_username"]
        password=request.POST["instagram_password"]
        control_instagram_user=Instagram_Accounts.objects.filter(username=username)
        if len(control_instagram_user)==0:
            check_user=private_api.check_is_real(username,password)
            #check_is_real Authentication da hatası verebilir. 
            #Hesap eklerken lazım olacak doğrulama işlerini de bu fonksiyonda halledelim.
            if check_user==True:
                New_IG_Account=Instagram_Accounts(username=username,password=password,is_current_account=1)
                #eklemiş olduğu diğer hesapları, varsa, is_current_account = 0 şeklinde değiştirelim.
                user=User.objects.get(username=request.user)
                New_IG_Account.main_user=user
                New_IG_Account.save()
                #Analiz başlatma ve info alma
                info = private_api.get_analysis(New_IG_Account)
                return render(request,"profile.html",{"wow":"none","wow2":"block","instagram_username":username,"follower_count"
                :info[7],"following_count":info[11],"media_count":info[10]})
            else:
                return render(request,"profile.html",{"wow":"block","wow2":"none","hata":"Kullanıcı adı veya şifre hatalı"})
        else:
            return render(request,"profile.html",{"wow":"block","wow2":"none","hata":"Bu hesap zaten kayıtlı"})


def profile(request):
    return render(request,"profile.html",{"wow":"none","wow2":"block","hata":"hata","user":request.user})

def islemler(request):
    return render(request,"takip,yorum,beğeni.html")

def takip(request):
    return render(request,"kişi,lokasyon,hashtag.html",{"islem":"takip"})

def yorum(request):
    return render(request,"kişi,lokasyon,hashtag.html",{"islem":"yorum"})

def begeni(request):
    return render(request,"kişi,lokasyon,hashtag.html",{"islem":"begeni"})

def create_assistant(request,id):
    if request.POST:
        instagram_user_or_hashtag_or_lokasyon=request.POST["instagram_user"]
        cb1=request.POST.get("cb1")
        cb2=request.POST.get("cb2")
        cb3=request.POST.get("cb3")
        try:
            cb0=request.POST.get("cb0")
            cb4=request.POST.get("cb4")
            r1=request.POST.get("r1")
            r2=request.POST.get("r2")
            r3=request.POST.get("r3")
            r4=request.POST.get("r4")
            r5=request.POST.get("r5")
        except:
            pass
        if cb0==None:
            cb0=0
        else:
            cb0=1
        if cb1==None:
            cb1=0
        else:
            cb1=1
        if cb2==None:
            cb2=0
        else:
            cb2=1
        if cb3==None:
            cb3=0
        else:
            cb3=1
        if cb4==None:
            cb4=0
        else:
            cb4=1
        if r1==None:
            r1=0
        else:
            r1=1
        if r2==None:
            r2=0
        else:
            r2=1
        if r3==None:
            r3=0
        else:
            r3=1
        if r4==None:
            r4=0
        else:
            r4=1
        if r5==None:
            r5=0
        else:
            r5=1
        try:
            yorum=request.POST["yorum"]
        except:
            yorum=None
        try:
            takip_sayısı=request.POST["takip_sayisi"]
        except:
            takip_sayısı=None
        try:
            begeni_sayisi=request.POST["begeni_sayisi"]
        except:
            begeni_sayisi=None
        varsayılan_ayarlar=request.POST.get("varsayılan_ayarlar")
        if varsayılan_ayarlar==None:
            varsayılan_ayarlar=0
        else:
            varsayılan_ayarlar=1
        try:
            max_takipci_sayısı=request.POST["max_takipci_sayısı"]
            min_takipci_sayısı=request.POST["min_takipci_sayısı"]
            max_takip_sayısı=request.POST["max_takip_sayısı"]
            min_takip_sayısı=request.POST["min_takip_sayısı"]
            max_gönderi_sayısı=request.POST["max_gönderi_sayısı"]
            min_gönderi_sayısı=request.POST["min_gönderi_sayısı"]
            gizli_hesap=request.POST.get("gizli_hesap")
            biyografi=request.POST.get("biyografi")
            profil_resmi=request.POST.get("profil_resmi")
            isletme_hesapları=request.POST.get("isletme_hesapları")
        except:
            pass
        yavas=request.POST.get("yavas")
        orta=request.POST.get("orta")
        hızlı=request.POST.get("hızlı")
        islem_hızı=0
        if gizli_hesap==None:
            gizli_hesap=0
        else:
            gizli_hesap=1
        if biyografi==None:
            biyografi=0
        else:
            biyografi=1
        if profil_resmi==None:
            profil_resmi=0
        else:
            profil_resmi=1
        if isletme_hesapları==None:
            isletme_hesapları=0
        else:
            isletme_hesapları=1
        if yavas=="on":
            islem_hızı=1
        if orta=="on":
            islem_hızı=2
        if hızlı=="on":
            islem_hızı=3
        if id==1 or id==2 or id==3:
            if id==1:
                assistant_action_type=1
            elif id==2:
                assistant_action_type=2
            else:
                assistant_action_type=3
            assistant_source_type=1
        elif id==4 or id==5 or id==6:
            if id==4:
                assistant_action_type=1
            elif id==5:
                assistant_action_type=2
            else:
                assistant_action_type=3
            assistant_source_type=2
        else:
            if id==7:
                assistant_action_type=1
            elif id==8:
                assistant_action_type=2
            else:
                assistant_action_type=3
            assistant_source_type=3


        instagram_account=Instagram_Accounts.objects.get(main_user__username=request.user)
        assistant=Assistants(instagram_account=instagram_account,assistant_source_type=assistant_source_type,assistant_action_type=assistant_action_type)
        assistant.save()

        assistant_settings=Assistants_Settings(assistant=assistant,min_followers=min_takipci_sayısı,max_followers=max_takipci_sayısı,min_followings=min_takip_sayısı,
        max_followings=max_takip_sayısı,is_hidden=gizli_hesap,biography=biyografi,is_business=isletme_hesapları,max_posts=max_gönderi_sayısı,
        min_posts=min_gönderi_sayısı)
        assistant_settings.save()


        if assistant_source_type==1:
            if assistant_action_type==1:
                assistant_user=Assistant_User(assistant=assistant,username=instagram_user_or_hashtag_or_lokasyon,followers=cb1,
                followings=cb2,likers=cb3,commenters=cb4)
                assistant_user.save()
            if assistant_action_type==2:
                assistant_user=Assistant_User(assistant=assistant,username=instagram_user_or_hashtag_or_lokasyon,own=cb0,followers=cb1,
                followings=cb2,likers=cb3,commenters=cb4)
                assistant_user.save()
            else:
                assistant_user=Assistant_User(assistant=assistant,username=instagram_user_or_hashtag_or_lokasyon,own=cb0,followers=cb1,
                followings=cb2,likers=cb3,commenters=cb4)
                assistant_user.save() 
        if assistant_source_type==2:
            assistant_hashtag=Assistant_Hashtag(assistant=assistant,hashtag=instagram_user_or_hashtag_or_lokasyon,posters=cb1,commenters=cb2,likers=cb3)
            assistant_hashtag.save()
        else:
            assistant_location=Assistant_Location(assistant=assistant,location=instagram_user_or_hashtag_or_lokasyon,posters=cb1,commenters=cb2,likers=cb3)
            assistant_location.save()
    
    return render(request,"dashboard.html")


def takip_kisi(request):
    return render(request,"kisi_takip.html")

def takip_hashtag(request):
    return render(request,"hashtag_takip.html")

def takip_lokasyon(request):
    return render(request,"lokasyon_takip.html")

def begeni_hashtag(request):
    return render(request,"hashtag_begeni.html")

def begeni_kisi(request,id):
    return render(request,"kisi_begeni.html")

def begeni_lokasyon(request):
    return render(request,"lokasyon_begeni.html")

def yorum_hashtag(request):
    return render(request,"hashtag_yorum.html")

def yorum_kisi(request,id):
    return render(request,"kisi_yorum.html")

def yorum_lokasyon(request):
    return render(request,"lokasyon_yorum.html")
