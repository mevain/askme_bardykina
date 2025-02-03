"""
URL configuration for askme_bardykina project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app import views
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('questions/<int:question_id>', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('hot', views.hot, name='hot'),
    path('signup', views.signup, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('tag/<str:tag_name>', views.tag, name='tag')
]
