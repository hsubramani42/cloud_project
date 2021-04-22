from django.urls import path
from . import views as v1, viewAdmin as v2, viewMember as v3
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',v1.homepage,name="index"),
    path('signup/',v1.signup,name="register"),
    path('events/',v1.events,name="event"),
    path('about-us/',v1.about,name="about"),
    path('login/',v3.login,name="login"),
    path('home/',v3.logged,name='home'),
    path('tackle/',v3.tackle,name='tackle'),
    path('attendance/',v3.attendance,name='attendanceCheck'),
    path('feedback/',v3.feedback,name='feedback'),
    path('event/',v3.events,name='eventRegister'),
    path('profile/',v3.profile,name='profile'),
    path('delete/',v3.delete,name='delete'),
    path('logout/',v3.logout,name='logout'),
    path('feedbackView/',v2.feedback,name='feedbackView'),
    path('administrator/',v2.administrator,name="administrator"),
    path('adminDashboard/',v2.adminLogin,name="adminDashboard"),
    path('adminApprove/',v2.adminApprove,name="approve"),
    path('adminEvent/',v2.adminEvent,name="upload"),
    path('adminAttendance/',v2.adminAttendance,name="attendance"),
    path('adminLogout/',v2.adminLogout,name="adminLogout"),
    path('data/',v2.data,name="data"),
    path('download/<path:filename>',v2.download,name="datadownload"),
    path('media/data/<path:path>',v3.download,name='download'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
