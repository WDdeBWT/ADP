# coding: utf-8

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

# Create your views here.


class ExperimentListView(View):
    def get(self, request):
        return render(request, 'exp_list.html', {

        })