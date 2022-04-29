from django.urls import path
from django.contrib import admin
from seller import views

app_name = 'seller'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('become-seller/', views.becomeSeller, name='become-seller'),
    path('login/', views.loginView, name='login'),
    path('register/', views.register, name='register'),
    path('change-password/', views.changePassword, name='change-password'),
    path('logout/', views.logout_, name='logout'),
    path('change-usrpic/',views.change_usrpic,name='change-usrpic'),
    path('delete-account/', views.delete_account, name='delete-account')
    
]
