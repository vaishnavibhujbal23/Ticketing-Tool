from django.urls import path
from .views import register,ticket_list,ticket_detail,create_ticket,update_ticket_status,manage_tickets,assign_engineer
urlpatterns = [
    path('',register, name='register'),
    path('register/',register, name='register'),
    path('ticket_list/',ticket_list,name='ticket_list'),
    path('ticket_detail/<int:pk>/',ticket_detail,name='ticket_detail'),
    path('create_ticket/',create_ticket,name='create_ticket'),
    path('update_ticket_status/<int:pk>/',update_ticket_status,name='update_ticket_status',),    
    path('manage_tickets/', manage_tickets, name='manage_tickets'),
    path('assign_engineer/<int:pk>/', assign_engineer, name='assign_engineer'),
]
