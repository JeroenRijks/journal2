"""learnjournal URL Configurationneric message. And a lot has changed since this question was posted. No more 32-bit versions are considered modern, for one. I posted the simple answer below that works in July 2017. Simply install that modul

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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('journal.urls', namespace='journal')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
