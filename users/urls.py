from django.urls import path, include

from .views import *


app_name='users'
# bunu ilk yaptık,
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    # burda tabi siteadı.com./users/register/ burda ki
    # users fantom.urls'den geliyor
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),


]
