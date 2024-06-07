from django.urls import path
from . import views

urlpatterns = [
    path("scraping_status", views.GetJobData, name="hello"),
    path("start_scraping", views.StartScraping, name="start_scraping")
]