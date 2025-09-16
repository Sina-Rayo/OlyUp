from django.urls import path
from . import views

app_name = "verification"

urlpatterns = [
    path('correct' , views.create_solution)
]
