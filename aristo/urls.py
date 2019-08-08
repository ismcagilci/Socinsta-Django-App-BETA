from django.contrib import admin
from django.urls import path
from aristo import views


app_name="aristo"

urlpatterns = [
    path('',views.landing),
    path('login/',views.login_user),
    path('register/',views.register),
    path('pricing/',views.pricing),
    path('logout/',views.logout_user),
    path('dashboard/',views.dashboard),
    path('profile/',views.profile),
    path('islemler/',views.islemler),
    path('takip/',views.takip),
    path('yorum/',views.yorum),
    path('begeni/',views.begeni),
    path('create_assistant<int:id>',views.create_assistant),
    path('takip/kişi',views.takip_kisi),
    path('takip/hashtag',views.takip_hashtag),
    path('takip/lokasyon',views.takip_lokasyon),
    path('begeni/kişi<int:id>',views.begeni_kisi),
    path('begeni/lokasyon',views.begeni_lokasyon),
    path('begeni/hashtag',views.begeni_hashtag),
    path('yorum/kişi<int:id>',views.yorum_kisi),
    path('yorum/hashtag',views.yorum_hashtag),
    path('yorum/lokasyon',views.yorum_lokasyon),
    path('add_insta_account',views.add_insta_account)



]
