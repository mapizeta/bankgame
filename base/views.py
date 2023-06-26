from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView, View
from base.models import Game,Transaction,Gamer,Statistic
from django.views.generic.base import RedirectView
from django.shortcuts import render

class Index(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
            
        context['game_list'] = Game.objects.all()
        context['transactions'] = Transaction.objects.all()
        
        return context

class Home(View):

    def get(self, request, *args, **kwargs):
        context = {}
        print('request',request)
        print('kwargs',kwargs)
        
        gamer = Gamer.objects.filter(
            nickname=self.request.GET['username'],
            password=self.request.GET['password'])
        
        if len(gamer) > 0:
            gamerObject = gamer[0]
        else:
            return HttpResponseRedirect('/?error=1')
        
        context['user'] = Statistic.objects.filter(gamer=gamerObject.id)

        if len(context['user']) == 0:
            return HttpResponseRedirect('/?error=2')
        else:
            context['gamer_list'] = Statistic.objects.filter(game=gamerObject.actual).exclude(gamer=gamerObject)
            context['transactions'] = Transaction.objects.all()
        
        return render(request,'home.html', context)

class TransactionRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "home"

    def get_redirect_url(self, *args, **kwargs):
        print(self.request.GET)
        sender = Gamer.objects.get(pk=self.request.GET['sender'])
        receiver = Gamer.objects.get(pk=self.request.GET['receiver'])
        transaction = Transaction()
        transaction.sender = sender
        transaction.receiver = receiver
        transaction.amount = int(self.request.GET['monto'])
        transaction.save()

        return super().get_redirect_url(*args, **kwargs)

class loginRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "index"

    def get_redirect_url(self, *args, **kwargs):
        print(self.request.GET)
        return super().get_redirect_url(*args, **kwargs)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
