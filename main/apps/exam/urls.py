from django.urls import path
#DO this!!!!! up above
from . import views

urlpatterns = [
    path('',views.index),
    path('validate',views.validate),
    path('log',views.log),
    path('login',views.login),
    path('addjob', views.addpg),
    path('addprocess',views.addp),
    path('vprocess/<int:jid>',views.vprocess),
    path('logout',views.logout),
    path('addtomyjobs/<int:jid>',views.addtomyjobs),
    path('delete/<int:jid>',views.remove),
    path('del/<int:id>',views.deletejob),
    path('edit/<int:id>',views.edit),
    path('editprocess/<int:id>',views.editprocess),
]