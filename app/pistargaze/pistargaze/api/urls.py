from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from . import views

urlpatterns = [
	url(r'command/power$', views.UtilsPower.as_view(), name='Command'),
]