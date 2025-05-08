from django.urls import path
from . import views
urlpatterns = [
     path('',views.homeView,name='home'),
     path('about/',views.aboutView, name='about'),
     path('services/',views.servicesView, name='servies'),
     path('calculator/',views.calculatorView,name='calculator'),
     path('contact/',views.Contact.as_view(),name='contact'),
     path('disclaimer/',views.DisclaimerView,name='disclaimer'),
     path('policy/',views.PolicyView,name='policy'),
     path('terms/',views.TermView,name='terms'),
]
