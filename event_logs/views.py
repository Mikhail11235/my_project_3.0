from django.views.generic import ListView
from . models import ModelImage
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import Form

class CsvFileDetailView(ListView):
    model = ModelImage
    template_name = 'detail.html'

    def get_queryset(self):
        return ModelImage.objects.order_by('-pk')[0]


def get_file_and_type(request):
    if request.method == 'POST':
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            instance = ModelImage.objects.create(file_id = post.id)
            instance.save()
            if post.file_is_valid():
                return HttpResponseRedirect(reverse_lazy('detail'))
            else:
                form = Form()
    else:
        form = Form()

    return render(request, 'home.html', {'form': form}) 