from django.shortcuts import render
# from django.template.response import RequestContext
from django.views.generic import View

from elasticsearch_dsl import Search

from main.forms import SearchForm


class HomeView(View):
    
    def get(self, request):
        
        form = SearchForm(request.GET)
        
        ctx = {
            "form": form
        }
    
        if form.is_valid():           
            name_query = form.cleaned_data["name"]
            
            if name_query:
                s = Search(index="daintree").query("match", name=name_query)
            else:
                s = Search(index="daintree")
            
            result = s.execute()
            
            ctx["products"] = result.hits
            
        return render(request, "main/home.html", ctx)
