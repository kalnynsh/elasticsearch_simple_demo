from django.shortcuts import render
# from django.template.response import RequestContext
from django.views.generic import View

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from main.forms import SearchForm


class HomeView(View):
    
    def get(self, request):
        
        form = SearchForm(request.GET)
        
        ctx = {
            "form": form
        }
    
        if form.is_valid():
            connections.create_connection()
            
            name_query = form.cleaned_data["name"]
            s = Search(index="daintree").query("match", name=name_query)
            
            result = s.execute()
            
            ctx["products"] = result.hits
            
        return render(request, "main/home.html", ctx)
