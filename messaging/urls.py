from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("<int:conversation_id>/", views.conversation_detail, name="conversation"),
    path("nouveau/<int:user_id>/", views.start_conversation, name="start_conversation"),
]
