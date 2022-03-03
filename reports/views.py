from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from profiles.models import Profile
from .utils import get_report_image
from .models import Report

class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'

def create_report_view(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = get_report_image(request.POST.get('image'))
        author = Profile.objects.get(user=request.user)

        Report.objects.create(name=name, remarks=remarks, image=image, author=author)

        return JsonResponse({'message': 'sent'})
    return JsonResponse({})
