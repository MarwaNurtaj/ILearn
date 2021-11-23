from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    


    path('',views.homepage, name="homepage"),
    path('home/', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('account/',views.accountSettings, name="account"),
    path('courses/', views.courses,name="courses"),
    path('students/<str:pk_test>/', views.students,name="students"),
    path('teacheraccount/',views.teacherSettings, name="teacheraccount"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('webdesign/', views.webdesign,name="webdesign"),
    path('electric/', views.electric,name="electric"),
    path('calculations/', views.calculations,name="calculations"),
    path('english/', views.english,name="english"),
    path('aboutus/', views.aboutus,name="aboutus"),
    path('support/', views.support,name="support"),

 
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),

     path('chathome',views.chathome,name='chathome'),
     path('<str:room>/', views.room, name='room'),
     path('checkview',views.checkview,name='checkview'),
     path('send',views.send,name='send'),
     path('getMessages/<str:room>/', views.getMessages, name='getMessages'),    
    path('index',views.index,name='index'),
    path('login2',views.login2,name='login2'),
]