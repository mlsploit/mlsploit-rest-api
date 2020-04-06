"""api URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from api.settings import MEDIA_DIR, MEDIA_URL
from files.views import FileViewSet
from modules.views import FunctionViewSet, ModuleViewSet
from pipelines.views import PipelineViewSet, TaskViewSet, RunViewSet, JobViewSet
from users.views import UserViewSet


router = routers.DefaultRouter()
router.register(r"modules", ModuleViewSet)
router.register(r"functions", FunctionViewSet)
router.register(r"users", UserViewSet, basename="user")
router.register(r"files", FileViewSet, basename="file")
router.register(r"pipelines", PipelineViewSet, basename="pipeline")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"runs", RunViewSet, basename="run")
router.register(r"jobs", JobViewSet, basename="job")

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^auth/", include("rest_auth.urls")),
    url(r"^auth/registration/", include("rest_auth.registration.urls")),
    url(r"^api/v1/", include(router.urls)),
    url(r"^docs/", include_docs_urls(title="MLsploit API")),
] + static(MEDIA_URL, document_root=MEDIA_DIR)
