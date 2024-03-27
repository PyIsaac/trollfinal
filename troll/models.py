from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Credit

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})


class Fight(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	Matchfield = models.TextField(default="")
	selected = models.IntegerField(default=0)
	messageback = models.TextField(default="")
	secondredir = models.TextField(default="")


	def get_info(self):
		return self.Matchfield






