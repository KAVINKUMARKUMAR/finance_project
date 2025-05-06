from django.urls import path
from . import views
urlpatterns = [
     path('',views.homeView,name='home'),
     path('about/',views.aboutView, name='about'),
     path('services/',views.servicesView, name='servies'),
     path('calculator/',views.calculatorView,name='calculator'),
     path('contact/',views.Contact.as_view(),name='contact'),
]
