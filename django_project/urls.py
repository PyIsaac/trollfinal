"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('', include('troll.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
        name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
    path('crypto/', user_views.play_game, name='crypto'),
    path('about/', user_views.about, name ='users-about'),
    path('thorton/', user_views.thorton, name='thorton'),
    path('leaderboard/', user_views.highscores, name='leader'),
    path('aboutstart/', user_views.aboutstart, name='aboutstart'),
    path('about/aboutstart/', user_views.aboutstart1, name='aboutstart1'),
    path('leaderboard/aboutstart/', user_views.aboutstart2, name='aboutstart2'),
    path('posts/aboutstart/', user_views.aboutstart3, name='aboutstart3'),
    path('shop/aboutstart/', user_views.aboutstartcry, name='aboutstartshop'),
    path('end/aboutstart/', user_views.aboutstart4, name='aboutstart4'),
    path('help/', user_views.aboutstarthelp, name='aboutstarthelp'),
    path('leaderboard/2000+/', user_views.reached2000, name='reached2000'),
    path('leaderboard/2000+/congrats', user_views.reached2000congrats, name='r2000c'),
    path('shop/cryptpoweb/', user_views.robbuy, name='buycry'),
    path('trn/<int:pk>/', user_views.transfer_score, name='transfer_score'),
    path('robbed/', user_views.robbed, name='robbed'),
    path('shop/', user_views.shop, name='shop'),
    path('shop/success', user_views.success, name='succ'),
    path('splitorsteal/', user_views.splitorsteal, name='splitorsteal'),
    path('splitorstealreal/<int:pk>/<int:pk1>/', user_views.splitorstealreal, name='splitorstealreal'),
    path('splitorstealreal/<int:pk>/<int:pk1>/waitingroom', user_views.splitorstealwait, name='splitorstealwait'),
    path('splitorstealreal/<int:pk>/<int:pk1>/final', user_views.splitorstealfinal, name='splitorstealfinal'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

