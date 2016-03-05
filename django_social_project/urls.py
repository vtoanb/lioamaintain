"""django_social_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
#from django_social_app.views import AnalyticsIndexView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django_social_project import settings

admin.autodiscover()

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', 'django_social_app.views.maintainlist'),
    url(r'^home/$', 'django_social_app.views.home'),
    url(r'^logout/$', 'django_social_app.views.logout'),
    url(r'^chart$', 'django_social_app.views.login'),
    url(r'^ajaxtest/$', 'django_social_app.views.viewajaxtest'),
    url(r'^ajaxupdate/$', 'django_social_app.views.viewajaxupdate'),
    url(r'^ajax30dayenergy/$', 'django_social_app.views.getLatest30DaysEnergy'),
    url(r'^ajaxprevday/$'    , 'django_social_app.views.getPrevDay'),
    url(r'^ajaxgetmonth/$','django_social_app.views.getFirstMonth'),
    url(r'^ajaxdomaintain/$','django_social_app.views.getDoMaintain'),
    url(r'^updatemaintain/$','django_social_app.views.updateMaintain'),
    url(r'^ajaxupdatetable/$','django_social_app.views.updateTable'),
    url(r'^ajaxlogin/$','django_social_app.views.ajaxloginview'),
    url(r'^ajaxexpanddetail/$','django_social_app.views.ajaxexpanddetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
""" both for static files handling """
urlpatterns += staticfiles_urlpatterns()
