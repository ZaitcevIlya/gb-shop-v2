
from django.urls import path
# from authapp.views import
from authapp.views import ProfileFormView, LoginListView, RegisterListView, Logout, GoogleAuth

app_name = 'authapp'
urlpatterns = [

    path('login/', LoginListView.as_view(),name='login'),
    path('register/', RegisterListView.as_view(),name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),
    # Google Auth
    path("all/", GoogleAuth.as_view(), name="all"),

    path('verify/<str:email>/<str:activate_key>/', RegisterListView.verify, name='verify'),
]
