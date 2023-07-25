import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from datetime import timedelta, date, datetime
import random
from django.utils import timezone
from .models import Post, Credit, DateTimeEncoder
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
from django.http import HttpResponseBadRequest
import time
from django.views.generic import ListView
from troll.views import Post as Posttroll


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, You are able to login now')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    try:
        credit_obj = Credit.objects.get(user=request.user)
        score = credit_obj.score
    except Credit.DoesNotExist:
        score = 0  # Set a default score if the user does not have a Credit object

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'score': score,
    }

    return render(request, 'users/profile.html', context)

class DateTimeEncoderExtra(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat() # convert to string using isoformat()
        return super().default(obj)




@login_required
def play_game(request):
    user = request.user
    game = play_game
    top_scores = Credit.objects.order_by('-score')[:10]
    messages.warning(request, 'After you invest your score, it will take 14 seconds to update so you can leave for then.')
    try:
        score_obj = Credit.objects.get(user=request.user)
        score = score_obj.score
        date_created = timezone.now() - score_obj.date_posted
        score_obj.save()
    except Credit.DoesNotExist:
        score = 100
        score_obj = Credit(user=user, score=score, date=timezone.now())
        score_obj.save()
        date_created = timezone.now() - score_obj.date_posted

    except json.JSONDecodeError:
        score_obj = Credit.objects.filter(user=user).latest('date_posted')
        score = score_obj.score
        date_created = timezone.now() - score_obj.date_posted


    invested = None
    #date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #data1 = request.body.decode('utf-8')#--contains nothing?
    context = {}
    if request.method == 'POST':

        daylater = score_obj.daylater
        if date_created >= timedelta(seconds=14):
            daylater = True
            score_obj.date = timezone.now()
            score_obj.save()
        #try:
        #json_data1 = json.dumps(str(date), cls=DateTimeEncoderExtra)#---------------------------------------------------------------------------------------------------------<
        #dates = json.loads(json_data1)
        #except json.JSONDecodeError:
            #date = ()
            #return HttpResponseBadRequest(date, 'Invalid JSON data in request body')


        # get the start and end date from the data
        #now = datetime.datetime.now()
        #data = {'current_time': now}
        #startdate = serializers.serialize('json', [data])
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        data = {'current_time': formatted_date}
        startdate = datetime(2023, 4, 28, 15, 30, 45) #request.POST.get('startdate', '2023-04-23')
        enddate = () #request.POST.get('enddate', '2023-04-24')
        if startdate is not None:
            

            i = True
            #startdate_obj = json_data1
            #enddate_obj = datetime.strptime(enddate, '%Y-%m-%d')



            # check if the end date is greater than the start date
            if i is False:
                context['error'] = "End date must be greater than start date."
            else:

                playerinput = float(request.POST.get('player_input', 0))
                
                game = Game(score, playerinput)


                if game.invested(playerinput):

                    request.session['invested'] = playerinput
                    request.session['last_action'] = str(timezone.now())

                    

                    updated_score = game.get_updated_score()
                    if updated_score is False:
                        context['error'] = "You don't have enough credit."

                    else:

                        """score = updated_score
                        score_obj.score = score
                        score_obj.save()
                        context['result'] = "Your score is now {}.".format(score)
                        context['score'] = score"""
                        time.sleep(2)
                        if daylater:


                            progress = game.get_progress()

                            #end = progress + score
                            score_obj.score = progress
                            #messages.warning(request, 'Warning message here.')

                            time.sleep(5)

                            if score_obj.scoreback == -1:
                                score_obj.aboutstart = True
                            score_obj.save()
                            score11 = Credit.objects.get(user=user)
                            score11.scoreback = game.progresstrack()

                            score11.scorebackinfo = context['result'] = "Your score is now {}.".format(progress)
                            score11.scorebackreal = game.scorebackrl()
                            score11.save()
                            if score_obj.aboutstart:
                                return redirect('aboutstart')
                            else:
                                return redirect('users-about')

                        else:

                            end = game.get_updated_score()
                            score_obj.score = end
                            score_obj.save()
                            return HttpResponseBadRequest("game.get_progress(")

                            
                        
                else:
                    context['error'] = 'Not enough credit to invest'
        else:
            context['error'] = "Please provide start and end dates."
            startdate_obj = None

    else:
        invested = request.session.get('invested', 2)
        last_action = request.session.get('last_action')
        startdate_obj = None
        startdate = None
        data = (score_obj.date)

        """if invested and last_action and timezone.now() - last_action >= timedelta(seconds=5):
            request.session['invested'] = 0
            request.session['last_action'] = None
            if score:
                context['score'] = score"""
    #request.session['score'] = score_obj.score
    daylater = True
    if date_created >= timedelta(seconds=14):
        daylater = True
        score_obj.date = timezone.now()
        score_obj.save()
        score_obj.save()
        my_instance = Credit()
        my_instance.update_score()
        context['score'] = score_obj.score

        context['daylater'] = daylater

        enddata = {
            'datetime': request.session.get('last_action'),
            'context': context,
            'scores': top_scores
        }
        json_data = json.dumps({'data':str(enddata)}, cls=DateTimeEncoderExtra)

        #def returner():
            #return render(request, 'users/play_game.html', context) #and redirect('troll-about')
        return HttpResponse(json_data, content_type='application/json') and render(request, 'users/play_game.html', context) # and redirect('troll-about')
        #returner()

class Game:
    def __init__(self, score1, player_input):
        self.player_input = player_input
        self.score1 = score1
        self.progress1 = 0
        self.ab = ""
        if self.score1 >= self.player_input:
            self.scoreback = float(self.score1 - self.player_input)
            self.check = True
        else:
            self.scoreback = float(self.score1)
            self.check = False

        if not self.check:
            print("You don't have enough credit.")


    def get_progress(self):
        chance = random.uniform(0.1, 1.8)

        if chance > 1:
            a = int((chance - 1) * 100)
            self.ab = "Stock grew by {}%.".format(a)
        else:
            a = int((1 - chance) * 100)
            self.ab = "Stock declined by {}%.".format(a)

        self.progress1 = self.player_input * chance
        progress = self.score1 + self.progress1  # update scoreback by adding progress1
        # progress = self.score1 - self.scoreback  # calculate the difference between score1 and scoreback
        print(progress)
        return progress


    def get_updated_score(self):
        if self.check:
            return self.scoreback
        else:
            return False


    def invested(self, amount):
        if amount <= self.score1:
            self.check = True
            self.scoreback = amount
            self.score1 -= amount
            return True
        else:
            return False


    def progresstrack(self):
        a = self.progress1
        return a
    def scorebackrl(self):
        return self.ab


class Thortongame:
    def __init__(self, score1, player_input):
        self.player_input = player_input
        self.score1 = score1
        self.progress1 = 0
        self.ab = ""
        if self.score1 >= self.player_input:
            self.scoreback = float(self.score1 - self.player_input)
            self.check = True
        else:
            self.scoreback = float(self.score1)
            self.check = False

        if not self.check:
            print("You don't have enough credit.")


    def get_progress(self):
        chance = random.uniform(0.6, 1.3)

        if chance > 1:
            a = int((chance - 1) * 100)
            self.ab = "Stock grew by {}%.".format(a)
        else:
            a = int((1 - chance) * 100)
            self.ab = "Stock declined by {}%.".format(a)

        self.progress1 = self.player_input * chance
        progress = self.score1 + self.progress1  # update scoreback by adding progress1
        # progress = self.score1 - self.scoreback  # calculate the difference between score1 and scoreback
        print(progress)
        return progress


    def get_updated_score(self):
        if self.check:
            return self.scoreback
        else:
            return False


    def invested(self, amount):
        if amount <= self.score1:
            self.check = True
            self.scoreback = amount
            self.score1 -= amount
            return True
        else:
            return False


    def progresstrack(self):
        a = self.progress1
        return a
    def scorebackrl(self):
        return self.ab


def about(request):
    a = Credit.objects.get(user=request.user)
    score = a.scoreback
    ano = a.scorebackinfo
    aa = a.scorebackreal

    context = {
        "info": score,
        "info2": ano,
        "info3": aa
    }
    return render(request, 'users/about.html', context)


@login_required
def thorton(request):
    game = thorton
    top_scores = Credit.objects.order_by('-score')[:10]
    user = request.user
    messages.warning(request, 'After you invest your score, it will take 14 seconds to update so you can leave for then.')
    try:
        score_obj = Credit.objects.get(user=request.user)
        score = score_obj.score
        date_created = timezone.now() - score_obj.date_posted
        score_obj.save()
    except Credit.DoesNotExist:
        score = 100
        score_obj = Credit(user=user, score=score, date=timezone.now())
        score_obj.save()
        date_created = timezone.now() - score_obj.date_posted

    except json.JSONDecodeError:
        score_obj = Credit.objects.filter(user=user).latest('date_posted')
        score = score_obj.score
        date_created = timezone.now() - score_obj.date_posted

    invested = None
    # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # data1 = request.body.decode('utf-8')#--contains nothing?
    context = {}
    if request.method == 'POST':

        daylater = score_obj.daylater
        if date_created >= timedelta(seconds=14):
            daylater = True
            score_obj.date = timezone.now()
            score_obj.save()
        # try:
        # json_data1 = json.dumps(str(date), cls=DateTimeEncoderExtra)#---------------------------------------------------------------------------------------------------------<
        # dates = json.loads(json_data1)
        # except json.JSONDecodeError:
        # date = ()
        # return HttpResponseBadRequest(date, 'Invalid JSON data in request body')

        # get the start and end date from the data
        # now = datetime.datetime.now()
        # data = {'current_time': now}
        # startdate = serializers.serialize('json', [data])
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        data = {'current_time': formatted_date}
        startdate = datetime(2023, 4, 28, 15, 30, 45)  # request.POST.get('startdate', '2023-04-23')
        enddate = ()  # request.POST.get('enddate', '2023-04-24')
        if startdate is not None:

            i = True
            # startdate_obj = json_data1
            # enddate_obj = datetime.strptime(enddate, '%Y-%m-%d')

            # check if the end date is greater than the start date
            if i is False:
                context['error'] = "End date must be greater than start date."
            else:

                playerinput = float(request.POST.get('player_input', 0))

                game = Thortongame(score, playerinput)

                if game.invested(playerinput):

                    request.session['invested'] = playerinput
                    request.session['last_action'] = str(timezone.now())

                    updated_score = game.get_updated_score()
                    if updated_score is False:
                        context['error'] = "You don't have enough credit."

                    else:

                        """score = updated_score
                        score_obj.score = score
                        score_obj.save()
                        context['result'] = "Your score is now {}.".format(score)
                        context['score'] = score"""
                        time.sleep(2)
                        if daylater:

                            progress = game.get_progress()

                            # end = progress + score
                            score_obj.score = progress
                            # messages.warning(request, 'Warning message here.')

                            time.sleep(5)
                            if score_obj.scoreback == -1:
                                score_obj.aboutstart = True
                            score_obj.save()
                            score11 = Credit.objects.get(user=user)
                            score11.scoreback = game.progresstrack()

                            score11.scorebackinfo = context['result'] = "Your score is now {}.".format(progress)
                            score11.scorebackreal = game.scorebackrl()
                            score11.save()
                            if score_obj.aboutstart:
                                return redirect('aboutstart')
                            else:
                                return redirect('users-about')

                        else:

                            end = game.get_updated_score()
                            score_obj.score = end
                            score_obj.save()
                            return HttpResponseBadRequest("game.get_progress(")



                else:
                    context['error'] = 'Not enough credit to invest'
        else:
            context['error'] = "Please provide start and end dates."
            startdate_obj = None

    else:
        invested = request.session.get('invested', 2)
        last_action = request.session.get('last_action')
        startdate_obj = None
        startdate = None
        data = (score_obj.date)

        """if invested and last_action and timezone.now() - last_action >= timedelta(seconds=5):
            request.session['invested'] = 0
            request.session['last_action'] = None
            if score:
                context['score'] = score"""
    # request.session['score'] = score_obj.score
    daylater = True
    if date_created >= timedelta(seconds=14):
        daylater = True
        score_obj.date = timezone.now()
        score_obj.save()
        score_obj.save()
        my_instance = Credit()
        my_instance.update_score()
        context['score'] = score_obj.score

        context['daylater'] = daylater

        enddata = {
            'datetime': request.session.get('last_action'),
            'context': context,
            'scores' : top_scores
        }
        json_data = json.dumps({'data': str(enddata)}, cls=DateTimeEncoderExtra)

        # def returner():
        # return render(request, 'users/play_game.html', context) #and redirect('troll-about')
        return HttpResponse(json_data, content_type='application/json') and render(request, 'users/thorton.html',
                                                                                   context)  # and redirect('troll-about')
        # returner()

def highscores(request):
    queryset = Credit.objects.order_by('-score')[:10]

    if queryset:
        first_credit = queryset[0]
        username = first_credit.user.username
        score = first_credit.score
    else:
        username = None
        score = None

    context = {
        'username': username,
        'score': score,
        'scores': queryset,
    }

    return render(request, 'users/highscores.html', context)

@login_required
def aboutstart(request):
    credit = Credit.objects.get(user=request.user)
    credit.aboutstart = False
    credit.save()

    return render(request, 'aboutstarts/aboutstart.html')
@login_required
def aboutstart1(request):
    a = Credit.objects.get(user=request.user)
    score = a.scoreback
    ano = a.scorebackinfo
    aa = a.scorebackreal

    context = {
        "info": score,
        "info2": ano,
        "info3": aa
    }
    return render(request, 'aboutstarts/aboutstart1.html', context)
@login_required
def aboutstart2(request):
    queryset = Credit.objects.order_by('-score')[:2]

    if queryset:
        first_credit = queryset[0]
        username = first_credit.user.username
        score = first_credit.score
    else:
        username = None
        score = None

    context = {
        'username': username,
        'score': score,
        'scores': queryset,
    }

    return render(request, 'aboutstarts/aboutstart2.html', context)
@login_required
def aboutstart3(request):
    context = {
        'posts': Posttroll.objects.all()[:2]
    }

    return render(request, 'aboutstarts/aboutstart3.html', context)
@login_required
def aboutstart4(request):

    return render(request, 'aboutstarts/aboutstart4.html')
@login_required
def aboutstarthelp(request):
    credit = Credit.objects.get(user=request.user)
    credit.aboutstart = False
    credit.scoreback = 0
    credit.save()
    return render(request, 'aboutstarts/aboutstarthelp.html')





