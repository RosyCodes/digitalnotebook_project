from django.urls import path
from . import views



urlpatterns = [
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('viewnotebook',views.viewnotebook,name='viewnotebook'),
    path('<int:notebook_id>',views.viewnotes,name='viewnotes'),
    path('createnotebook',views.createnotebook,name='createnotebook'),
    path('createnotebook/<int:notebook_id>',views.addnote,name='addnote'),
    path('deletenotebook/<int:notebook_id>',views.deletenotebook,name='deletenotebook'),
    path('updatenotebook/<int:notebook_id>',views.updatenotebook,name='updatenotebook'),
    path('editnote/<int:notebook_id>/<int:note_id>', views.editnote, name='editnote'),
    path('deletenote/<int:note_id>', views.deletenote, name='deletenote'),
    path('shared/<str:token>/', views.sharednotedetail, name='sharednotedetail'),
    path('share/<int:note_id>/', views.sharenote, name='sharenote'),

]
