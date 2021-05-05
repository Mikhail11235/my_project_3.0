from django.views.generic import ListView, CreateView
from . models import CsvFile
from django.urls import reverse_lazy
from .forms import PostForm


class CreatePostView(CreateView):
    model = CsvFile
    form_class = PostForm
    template_name = 'home.html'
    success_url = reverse_lazy('detail')


class CsvFileDetailView(ListView):
    model = CsvFile
    template_name = 'detail.html'

    def get_queryset(self):
        return CsvFile.objects.order_by('-pk')[0]