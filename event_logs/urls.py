from django.urls import path
from .views import get_file_and_type, CsvFileDetailView


urlpatterns = [
    path('', get_file_and_type, name='home'),
    path('detail/', CsvFileDetailView.as_view(), name='detail')
]