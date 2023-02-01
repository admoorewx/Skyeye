from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from pages.views import home_view
from .views import profile_view, login_user,logout_user, register_user, create_profile, edit_profile, view_profile

urlpatterns = [
    path('profile/',profile_view,name='profile'),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('register/',register_user,name='register_user'),
    path('create_profile/',create_profile,name='create_profile'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('view_profile/',view_profile,name='view_profile'),
    path('password_reset_sent/',auth_views.PasswordResetDoneView.as_view(template_name='authenticate/password_reset_done.html'),name='password_reset_sent'),
    path('password_reset_completed/',auth_views.PasswordResetCompleteView.as_view(template_name='authenticate/password_reset_complete.html'),name='password_reset_completed'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='authenticate/password_reset.html',success_url=reverse_lazy('password_reset_sent')),name='reset_password'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='authenticate/password_reset_confirm.html',success_url=reverse_lazy('password_reset_completed')),name='password_reset_confirm'),

] 
