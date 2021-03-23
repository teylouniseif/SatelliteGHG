from django.urls import path
from . import views

urlpatterns = [
    path('setTarget/', views.setTarget, name='setTarget'),
    path('setObservation/', views.setObservation, name='setObservation'),
    path('getTargets/', views.getTargets, name='getTargets'),
    path('getObservations/', views.getObservations, name='getObservations'),
    path('viewTargets/', views.viewTargets, name='viewTargets'),
    path('viewObservations/', views.viewObservations, name='viewObservations'),
]
