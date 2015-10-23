from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import View
from django_sse.views import BaseSseView
from django.utils.timezone import now
import time


def index(request):
    return render(request, 'index.html')