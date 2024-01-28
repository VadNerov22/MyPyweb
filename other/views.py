from django.shortcuts import render
from datetime import datetime

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render


class CurrentDateView(View):
    def get(self, request):
        html = f"{datetime.now()}"
        return HttpResponse(html)


class IndexView(View):
    def get(self, request):
        return render(request, 'other/index.html')