from django.shortcuts import render
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
            name_query = form.cleaned_data.get("name")
            
            if name_query:
                s = Search(index="daintree").query("match", name=name_query)
            else:
                s = Search(index="daintree")
            
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")
            
            if min_price is not None or max_price is not None:
                price_query = dict()
                
                if min_price is not None:
                    price_query["gte"] = min_price
                    
                if max_price is not None:
                    price_query["lte"] = max_price
                
                s = s.query("range", price=price_query)
            
            result = s.execute()
            
            ctx["products"] = result.hits
            
        return render(request, "main/home.html", ctx)
