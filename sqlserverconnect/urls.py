"""sqlserverconnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from sqlserverconnect.views import profileview
from sqlserverconnect.views.profileview import profile_view
from sqlserverconnect.views import changeprofilepictureview
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .views import views
from .views import searchview
from .views import reportview
from .views import changepasswordview

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.UserLoginView.as_view(), name = "admin_login"),
    path('logout/', views.logout_view, name = "logout"),
    path('home/',views.home,name="check_registration"),
    path('register/<int:appno>/<int:pageno>',views.register),
    path('search/',searchview.searchcategory),
    path('viewstudent/<int:appno>',reportview.view_student),
    path('classwisedetails/',searchview.classcategory),
    path('changepassword/',changepasswordview.change_password),
    path('changepp',changeprofilepictureview.changePP),
    path('profile/<int:pageno>',profileview.profile_view),
    #For importing student urls
    path('',include("student.urls")),
    #path('search/generateall',searchview.generateAll)
    #path('view',views.view_database),
    #path('viewimage',views.retrieve_image),
    #path('viewstudent/<int:appno>',views.view_student),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns=urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)