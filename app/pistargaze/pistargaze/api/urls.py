from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'command/power$', views.UtilsPower.as_view(), name='Command'),
	url(r'gps$', views.Position.as_view(), name='GPS'),
	url(r'command/telescope/slew', views.CommandTelescope.as_view(), name='Slew'),
	url(r'command/telescope/gpssync',view.SyncGPS.as_view(), name='GPSSync')
]