"""learnjournal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from journal import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^tag_list/$', views.TagList.as_view(), name='tag_list'),
    url(r'^deletetag/(?P<tag_id>[0-9]+)$', views.TagList.as_view(), name='deletetag'),
    url(r'^newresource/$', views.newresource, name='resource'),
    url(r'^newresource/(?P<res_id>[0-9]+)$', views.newresource, name='resource'),
    url(r'^deleteresource/(?P<res_id>[0-9]+)$', views.deleteresource, name='deleteresource'),
    url(r'^AJAX_tag_create/$', views.AJAX_tag_create, name='AJAX_tag_create'),
    url(r'^tag_edit/$', views.TagEdit.as_view(), name='tag_edit'),
    url(r'^tag_edit/(?P<tag_id>[0-9]+)$', views.TagEdit.as_view(), name='tag_edit'),

]
