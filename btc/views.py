from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Coinbar,Modelupdatetime
from .bedriver import getlastupdate

# Create your views here.
class BTCIndexView(generic.ListView):

    template_name = 'btc/BTCindex.html'
    context_object_name = 'BTC_Price_list'

    def get_queryset(self):
        return Coinbar.objects.filter(m_coin='btc').order_by('m_price')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        try:
            context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
            context['last_update_time'] = getlastupdate()
        except:
            pass
        return context

def index(request,coin_name='btc'):
    print("index",coin_name,request)
    coin_list = Coinbar.objects.filter(m_coin=coin_name).order_by('m_price')
    context = {'BTC_Price_list': coin_list,'coin_name':coin_name}
    return render(request, 'btc/BTCindex.html', context)