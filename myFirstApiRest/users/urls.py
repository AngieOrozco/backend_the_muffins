from django.urls import path 
from .views import UserRegisterView, UserListView, UserRetrieveUpdateDestroyView, UserProfileView, LogoutView,  ChangePasswordView, LoginView, MisSubastasView, MisPujasView 
 
app_name="users" 
urlpatterns = [ 
    path('register/', UserRegisterView.as_view(), name='user-register'), 
    path('', UserListView.as_view(), name='user-list'), 
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'), 
    path('profile/', UserProfileView.as_view(), name='user-profile'), 
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('log-out/', LogoutView.as_view(), name='log-out'),
    path('login/', LoginView.as_view(), name='login'),
    path('misSubastas/', MisSubastasView.as_view(), name='mis-subastas'),
    path('misPujas/', MisPujasView.as_view(), name='mis-pujas'),

] 