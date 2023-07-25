from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import admin
from django.contrib.auth import get_user_model
import json
from datetime import datetime, date




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Credit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=100)
    date = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(default=timezone.now())
    invested_score = models.IntegerField(default=0)
    owner_starts = models.BooleanField(default=True)
    daylater = models.BooleanField(default=False)
    scoreback = models.IntegerField(default=-1)
    scorebackinfo = models.TextField(default="")
    scorebackreal = models.TextField(default="")
    aboutstart = models.BooleanField(default=False)

    def update_score(self):
        if self.owner_starts and self.user is not None:
            # Retrieve the user's credit object from the database
            user_credit = Credit.objects.get(user=self.user)
            date_created = datetime.strptime(str(self.date), '%Y-%m-%d %H:%M:%S.%f%z')
            if datetime.now() - date_created >= timedelta(seconds=5):
                self.daylater = True
                user_credit.score -= self.invested_score
                user_credit.save()

class CreditAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date', 'date_posted')
    list_filter = ('date_posted',)
    search_fields = ('user__username',)

    def add_score(self, request, queryset):
        for credit in queryset:
            credit.score += 10
            credit.save()

    add_score.short_description = "Add 10 score to selected credits"
    actions = [add_score]


admin.site.register(Credit, CreditAdmin)



class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_posts')
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    content = models.TextField()
    score = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    invested_score = models.IntegerField(default=0)
    owner_starts = models.BooleanField(default=False)
    daylater = models.BooleanField(default=True)

    def __str__(self):
        return self.content

    def update_score(self):
        if self.owner_starts:
            date_created = self.date_posted
            if datetime.now() - date_created >= timedelta(days=1):
                self.daylater = True
                self.score -= self.invested_score
                self.save()



class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)