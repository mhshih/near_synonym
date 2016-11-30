#-*-coding:utf8-*-
from django.http import HttpResponse
from models import GRDS

def home(request,governor):
    rds=GRDS.objects.get(governor=governor).rds#'澤男').rds
    return HttpResponse(request.GET['callback']+'('+rds+')','text/javascript')
    return HttpResponse(rds)
