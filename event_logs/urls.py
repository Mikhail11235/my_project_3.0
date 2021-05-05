from django.urls import path
from .views import CreatePostView, CsvFileDetailView


urlpatterns = [
    path('', CreatePostView.as_view(), name='home'),
    path('detail/', CsvFileDetailView.as_view(), name='detail')
]