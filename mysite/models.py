from django.db import models

class User(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email_addr = models.CharField(max_length=100)
  
  def __str__(self):
    return self.email_addr


class Movie(models.Model):
  movie_name = models.CharField(max_length=50)
  num_stock = models.PositiveIntegerField()

  def __str__(self):
    return self.movie_name


class Checkout(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)