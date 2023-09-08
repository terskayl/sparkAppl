import json
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User, Post, PostComments, PostPictures

# Create your views here.
@csrf_exempt
def index(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			body = request.POST['body']
			post = Post(author=request.user, body=body)
			post.save()
			return render(request, 'dogstagram/index.html')
		return render(request, 'dogstagram/index.html')
	else:
		return HttpResponseRedirect(reverse('login'))

def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request, 'dogstagram/login.html', {
				'message' : 'Incorrect username or password'
			})
	return render(request, 'dogstagram/login.html')

def register(request):
	print('register')
	if request.method == 'POST':
		print('hi')
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']
		if password != password2:
			return render(request, 'dogstagram/register.html', {
				'message' : 'Passwords must match'
			})
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError as e:
			return render(request, 'dogstagram/register.html', {
				'message' : 'Username unavailable.'
			})
		login(request, user)
		return HttpResponseRedirect(reverse('index'))
	return render(request, 'dogstagram/register.html')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))


def package(request, posts):
	posts = posts.order_by("-timestamp").all()
	response = []
	for post in posts:
		postData = post.serialize()
		postData.update({'viewer': request.user.username})
		postData.update({'pfp' : post.author.pfp})
		postData.update({'images' : [pic.url for pic in post.pictures.all()] })
		postData.update({'comments' : [(comment.author.username, comment.body) for comment in post.comments.all()] })
		response.append(postData)
	return response

@csrf_exempt
def add(request):
	if request.method == 'POST':
		body = request.POST['body']
		post = Post(author=request.user, body=body)
		post.save()
		imageURL = request.POST['images']
		image = PostPictures(url=imageURL, onPost=post)
		image.save()
		return HttpResponseRedirect(reverse('index'))
	posts = Post.objects.all() #filter(author__in=request.user.following.all())
	posts = posts.order_by("-timestamp").all()
	return JsonResponse(package(request, posts), safe=False)

def createForm(request):
	return render(request, 'dogstagram/newPOst.html')


@csrf_exempt
def posts(request):
	if request.method == "PUT":
		data = json.loads(request.body)
		try:
			post = Post.objects.get(pk=data.get("id"))
		except Post.DoesNotExist:
			return JsonResponse({"error": "Post not found."}, status=404)
		if data.get("liked"):
			post.liked_by.add(request.user)
		else:
			post.liked_by.remove(request.user)
		post.save()
		return HttpResponse(status=204)
	posts = Post.objects.filter(author__in=request.user.following.all())
	return JsonResponse(package(request, tweets), safe=False)

@csrf_exempt
def comments(request):
	if request.method == "POST":
		id = request.POST['postId']
		try:
			post = Post.objects.get(pk=id)
		except Post.DoesNotExist:
			return JsonResponse({"error": "Post not found."}, status=404)
		comment = PostComments(author=request.user, body=request.POST['body'], post=post)
		comment.save()
		return HttpResponseRedirect(reverse('index'))
	return HttpResponseRedirect(reverse('index'))