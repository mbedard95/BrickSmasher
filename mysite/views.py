from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from mysite.models import User
from mysite.models import Movie
from mysite.models import Checkout
import json

class Home(View):
  def get(self, request):
    return render(request,"home.html",{})


class Account(View):
  def get(self, request):
    return render(request,"account.html",{})


class Manage(View):
  def get(self, request):
    return render(request,"manage.html",{})


class RentReturn(View):
  def get(self, request):
    return render(request,"rentreturn.html",{})


class Users(View):
  def get(self, request):
    email = request.GET.get("email",None).strip()
    if not email:
      return JsonResponse({"success":False,"message":"Please enter an email."})
    elif len(User.objects.filter(email_addr=email)) == 0:
      return JsonResponse({"success":False,"message":"No user found."})
    else:
      user = User.objects.filter(email_addr=email)[0]
      user_first = user.first_name
      user_last = user.last_name
      user_email = user.email_addr
      return JsonResponse({"success":True,"message":None,"first":user_first,"last":user_last,"email":user_email})
  def post(self, request):
    first = request.POST.get("first",None).strip()
    last = request.POST.get("last",None).strip()
    email = request.POST.get("email",None).strip()
    if not first or not last or not email:
      return JsonResponse({"success":False,"message":"Please fill out all fields."})
    elif len(User.objects.filter(email_addr=email)) > 0:
      return JsonResponse({"success":False,"message":"A user with this email already exists."})
    else:
      new_user = User(first_name=first,last_name=last,email_addr=email)
      new_user.save()
      return JsonResponse({"success":True,"message":"New user has been successfully added."})


class Movies(View):
  def get(self, request):
    all_movies = Movie.objects.all()
    all_movies = sorted(all_movies, key=str)
    movie_list = []
    for movie in all_movies:
      name = movie.movie_name
      num_stock = movie.num_stock
      id = movie.id
      num_checked_out = len(Checkout.objects.filter(movie=movie))
      movie_list.append("{\"movieName\":\""+name+"\",\"inStock\":"+str(num_stock)+",\"checkouts\":"+str(num_checked_out)+",\"id\":"+str(id)+"}") 
    return JsonResponse(json.dumps(list(movie_list)),safe=False)
  def post(self, request):
    action = request.POST.get("action",None)
    if action == "addMovie":
      movie_name = request.POST.get("movieName",None).strip()
      if not movie_name:
        return JsonResponse({"success":False,"message":"Please enter a movie title."})
      elif len(Movie.objects.filter(movie_name=movie_name)) > 0:
        return JsonResponse({"success":False,"message":"This movie already exists in the database."})
      else:
        new_movie = Movie(movie_name=movie_name, num_stock=1)
        new_movie.save()
        return JsonResponse({"success":True,"message":"New movie has been successfully added."})
    elif action == "addStock":
      movie_id = request.POST.get("movieId",None)
      this_movie = Movie.objects.filter(id=movie_id)[0]
      this_movie.num_stock += 1
      this_movie.save()
      return JsonResponse({"success":True,"message":None})
    elif action == 'removeStock':
      movie_id = request.POST.get("movieId",None)
      this_movie = Movie.objects.filter(id=movie_id)[0]
      if this_movie.num_stock > 0:
        this_movie.num_stock -= 1
        this_movie.save()
      return JsonResponse({"success":True,"message":None})

class Checkouts(View):
  def get(self,request):
    email = request.GET.get("email",None).strip()
    user = User.objects.filter(email_addr=email)[0]
    checkouts = Checkout.objects.filter(user=user)
    checkout_list = []
    if not checkouts:
      return JsonResponse(json.dumps(list(checkout_list)),safe=False)
    for item in checkouts:
      name = item.movie.movie_name
      id = item.movie.id
      checkout_list.append("{\"movieName\":\""+name+"\",\"id\":"+str(id)+"}") 
    return JsonResponse(json.dumps(list(checkout_list)),safe=False)
  def post(self,request):
    email = request.POST.get("email",None).strip()
    movie_id = request.POST.get("movieId",None)
    action = request.POST.get("action",None)
    movie = Movie.objects.filter(id=movie_id)[0]
    user = User.objects.filter(email_addr=email)[0]
    if action == "add":
      if len(Checkout.objects.filter(user=user,movie=movie)) > 0:
        return JsonResponse({"success":False,"message":"This user already has this movie checked out."})
      elif movie.num_stock == 0:
        return JsonResponse({"success":False,"message":"This movie is not in stock."})
      elif len(Checkout.objects.filter(user=user)) == 3:
        return JsonResponse({"success":False,"message":"This user already has three movies checked out."})
      else:
        new_checkout = Checkout(user=user,movie=movie)
        movie.num_stock -=1
        new_checkout.save()
        movie.save()
        return JsonResponse({"success":True,"message":"Checkout completed successfully."})
    if action == "delete":
      checkout = Checkout.objects.filter(user=user,movie=movie)[0]
      checkout.delete()
      movie.num_stock += 1
      movie.save()
      return JsonResponse({"success":True,"message":"Movie returned successfully."})
    