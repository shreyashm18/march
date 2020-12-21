from django.urls import path
from .views import RegisterUser, LogIn, LogOut, getUser
urlpatterns = [
    # path('register/', views.register,name = 'register'),
    path('register/', RegisterUser.as_view(),name = 'register'),
    path('login/', LogIn.as_view(),name = 'login'),
    path('logout/', LogOut.as_view(),name = 'logout'),
    path('getuser/', getUser.as_view(),name = 'getUser'),
]
