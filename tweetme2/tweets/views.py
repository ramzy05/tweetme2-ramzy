from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
import random



from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse('<h1>Hello World</h1>')
    return render(request,'pages/home.html', context = {}, status=200)

def tweet_create_view(request, *args, **kwargs):
    '''
    REST API Create View -> DRF
    '''
    user = request.user
    is_ajax = request.POST.get('is_ajax') or None
    if not request.user.is_authenticated:
        user = None
        if  is_ajax == 'true':
            return JsonResponse({},status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = user
        obj.save()
        if is_ajax == 'true':
            return JsonResponse(obj.serialize(), status=201)# 201 == create
        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if is_ajax == 'true':
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form':form}, status=200)

def tweet_list_view(request,*args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        'isUser':False,
        'response':tweets_list
    }
    return JsonResponse(data)
def tweet_detail_view(request, tweet_id,*args, **kwargs):
    """
    REST API VIEW
    Consume by Javascript or Swift/Java/iOS/Android
    return json data
    """
    data=  {
        'id':tweet_id
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content']=obj.content
    except:
        data['content'] ='Not found'
        status = 404
    return JsonResponse(data, status=status)