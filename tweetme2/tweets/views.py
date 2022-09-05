import random
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .forms import TweetForm
from .models import Tweet
from .serializers import (
    TweetSerializer,
    TweetActionSerializer,
    TweetCreateSerializer,
    )

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse('<h1>Hello World</h1>')
    return render(request,'pages/home.html', context = {}, status=200)

@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message':'You cannot delete this tweet'}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({'message':'Tweet removed'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args, **kwargs):
    '''

    id is required
    Action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data['id']
        action = data['action']
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()  
        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)  
        elif action == 'retweet':
            new_tweet = Tweet.objects.create(user=request.user,
            parent =obj,
          
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)        
    return Response({}, status=200)


@api_view(['GET'])
def tweet_list_view(request,*args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)






def tweet_create_view_pure_django(request, *args, **kwargs):
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

def tweet_list_view_pure_django(request,*args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        'isUser':False,
        'response':tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id,*args, **kwargs):
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