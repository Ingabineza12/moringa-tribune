import datetime as dt
from django.shortcuts import render,redirect
from .models import Article,Editor,tags, NewsLetterRecipients
#MoringaMerch === Article
from .forms import NewsLetterForm
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import NewArticleForm, NewsLetterForm
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import  ArticleSerializer
# MerchSerializer === ArticleSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly



# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')



# def news_today(request):
#     date = dt.date.today()
#     news = Article.todays_news()
#     form = NewsLetterForm(request.POST)
#     if request.method == 'POST':
#
#         if form.is_valid():
#             name = form.cleaned_data['your_name']
#             email = form.cleaned_data['email']
#
#             recipient = NewsLetterRecipients(name = name,email =email)
#             recipient.save()
#             send_welcome_email(name,email)
#
#             HttpResponseRedirect('news_today')
#         # else:
#         #      form = NewsLetterForm()
#     return render(request,'all-news/today-news.html',{"date": date,"news":news,"letterForm":form})

def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date, "news": news, "letterForm": form})

# View Function to present news from past days

# def news_of_day(request):
#     date = dt.date.today()
#     return render(request, 'all-news/today-news.html', {"date": date,})

def past_days_news(request, past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html',{"date": date,"news":news})

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})

@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newsToday')

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})


def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')
    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

# class MerchList(APIView):
#     def get(self, request, format=None):
#         all_merch = MoringaMerch.objects.all()  #  MoringaMerch === Article
#         serializers = MerchSerializer(all_merch, many=True)
#         return Response(serializers.data)
class MerchList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        all_articles = Article.objects.all()  #  MoringaMerch === Article
        serializers = ArticleSerializer(all_articles, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ArticleSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_merch(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = ArticleSerializer(merch)

    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = ArticleSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
