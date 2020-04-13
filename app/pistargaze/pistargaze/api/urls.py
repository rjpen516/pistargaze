from django.conf import settings
from django.conf.urls import include, url
from django.urls import path

from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'command/power$', views.UtilsPower.as_view(), name='Command'),
	url(r'gps$', views.Position.as_view(), name='GPS'),
	url(r'command/telescope/slew', views.CommandTelescope.as_view(), name='Slew'),
	url(r'command/telescope/gpssync',views.SyncGPS.as_view(), name='GPSSync'),
	url(r'command/telescope/status', views.TelescopeStatus.as_view(), name='TelescopeStatus'), 
	url(r'capture/latest', views.CaptureLatest.as_view(), name='CaptureLatest'),
	url(r'capture/analysis', views.CaptureAnalysis.as_view(), name='CaptureAnalysis'),
	url(r'capture/data', views.CaptureData.as_view(), name='CaptureData'),
	url(r'capture/calibrate', views.CaptureCalabration.as_view(), name='CaptureCalabration'),
	url(r'command/camera/stream', views.CameraStream.as_view(), name='CameraStream'),
	url(r'command/camera/capture', views.CameraCapture.as_view(), name='CameraCapture'),
	#url(r'session/new', views.SessionNewAPI.as_view(), name='SessionNew'),
	url(r'session/$', views.Sessions.as_view(), name="Sessions"),
	path(r'session/<str:pk>/', views.SessionsDetail.as_view(), name="SessionsDetail"),
	path(r'session/<str:pk>/setcurrent', views.SeesionsCurrent.as_view(), name="SessionCurrent"),
	path(r'session/<str:pk>/photos', views.SessionPhotos.as_view(), name="SessionPhotos"),
	path(r'photo/<str:token>/', views.PhotosLookup.as_view(), name="PhotoView"),

]