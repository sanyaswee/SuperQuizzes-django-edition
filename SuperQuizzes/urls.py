"""
URL configuration for SuperQuizzes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
import home.views
import account.views

urlpatterns = [

]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', home.views.index, name='index'),
    path('form/<id_>', home.views.form, name='form'),
    path('quiz', home.views.quiz_view, name='quiz'),
    path('result', home.views.result, name='result'),
    path('filter', home.views.filter_view, name='filter'),
    path('coming-soon', home.views.coming_soon, name='soon'),
    path('search', home.views.advanced_search, name='advanced_search'),
    path('register/', account.views.register_view, name='register'),
    path('login/', account.views.login_view, name='login'),
    path('logout/', account.views.logout_view, name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),

    prefix_default_language=True
)
