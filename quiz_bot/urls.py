
from django.contrib import admin
from django.urls import path, include
from core.views import chat

urlpatterns = [
    path("", chat, name="chat"),
    # path("admin/", admin.site.urls),
]
