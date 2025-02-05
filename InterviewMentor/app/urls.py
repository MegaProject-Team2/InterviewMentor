from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path("upload/", views.generate_questions, name="generate_questions"),
    path("chat/", views.chat_interface, name="chat_interface"),
    path("verify_answer/", views.verify_answer, name="verify_answer"),
    path('results/', views.save_answers, name='save_answers'),
    path('result/', views.result, name='result'),

]