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
from troll.models import Fight
from django.shortcuts import get_object_or_404
from .models import Profile

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
    user_scorecheck = Credit.objects.filter(user=user).values_list('score', flat=True).first()

    # Check if the user's score is greater than or equal to 2000

    game = play_game

    messages.warning(request, 'After you invest your score, it will take 14 seconds to update so you can leave for then.')
    try:
        score_obj = Credit.objects.get(user=request.user)
        score = score_obj.score
        date_created = timezone.now() - score_obj.date_posted
        if score_obj.score == 0:
            score_obj.score += 10
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

    if user_scorecheck and user_scorecheck >= 2000:
        if not score_obj.reached2000:
            reached_score_2000 = True
        else: reached_score_2000 = False
    else:
        reached_score_2000 = False
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
                            score_obj.invested_score = playerinput
                            score_obj.save()

                            score11 = Credit.objects.get(user=user)



                            score11.scoreback = game.progresstrack()

                            score11.scorebackinfo = context['result'] = "Your score is now {}.".format(progress)
                            score11.scorebackreal = game.scorebackrl()
                            score11.save()
                            ownsrob_status = Credit.objects.filter(ownsrob=True)
                            ownsrob_pks = [credit.user.pk for credit in ownsrob_status]

                            if ownsrob_pks:
                                firstrob_pk = ownsrob_pks[0]
                                score_obj.invested_score = playerinput
                                score_obj.save()
                                return redirect(f'/trn/{firstrob_pk}/')

                            if score_obj.aboutstart:
                                return redirect('aboutstart')

                            elif reached_score_2000:
                                return redirect('r2000c')
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
        }
        json_data = json.dumps({'data':str(enddata)}, cls=DateTimeEncoderExtra)

        #def returner():
            #return render(request, 'users/play_game.html', context) #and redirect('troll-about')
        return HttpResponse(json_data, content_type='application/json') and render(request, 'users/play_game.html', context) # and redirect('troll-about')
        #returner()

class Game:
    def __init__(self, score1, player_input):# inimese pragune skoor, inimese input
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
        chance = random.uniform(0.8, 1.8)

        if chance > 1:
            a = int((chance - 1) * 100)
            self.ab = "Stock grew by {}%.".format(a)
        else:
            a = int((1 - chance) * 100)
            self.ab = "Stock declined by {}%.".format(a)

        self.progress1 = self.player_input * chance
        progress = self.score1 + self.progress1
        falseprogress = self.score1# update scoreback by adding progress1
        # progress = self.score1 - self.scoreback  # calculate the difference between score1 and scoreback
        print(progress)
        ownsrob_status = Credit.objects.filter(ownsrob=True)
        ownsrob_pks = [credit.user.pk for credit in ownsrob_status]
        if ownsrob_pks:
            return falseprogress
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
    def rob(self):
        ownsrob_status = Credit.objects.filter(ownsrob=True)
        ownsrob = {'active_user_pks': [user.user.pk for user in ownsrob_status]}
        robdic = ownsrob['ownsrob']
        firstrob = robdic[0]
        return firstrob


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
        chance = random.uniform(0.1, 7.0)

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
    inv = a.invested_score

    aa = a.scorebackreal

    context = {
        "info": score,
        "invested": inv,
        "info2": ano,

        "info3": aa

    }
    return render(request, 'users/about.html', context)


@login_required
def thorton(request):
    game = thorton
    top_scores = Credit.objects.order_by('-score')[:10]
    user = request.user
    user_scorecheck = Credit.objects.filter(user=user).values_list('score', flat=True).first()


    # Check if the user's score is greater than or equal to 2000

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

    if user_scorecheck and user_scorecheck >= 2000:
        if not score_obj.reached2000:
            reached_score_2000 = True
        else: reached_score_2000 = False
    else:
        reached_score_2000 = False
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
                            score_obj.invested_score = playerinput
                            score_obj.save()
                            score11 = Credit.objects.get(user=user)
                            score11.scoreback = game.progresstrack()

                            score11.scorebackinfo = context['result'] = "Your score is now {}.".format(progress)
                            score11.scorebackreal = game.scorebackrl()
                            score11.save()
                            if score_obj.aboutstart:
                                return redirect('aboutstart')
                            elif reached_score_2000:
                                return redirect('r2000c')
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
@login_required
def aboutstartcry(request):

    return render(request, 'aboutstarts/aboutstartcryhook.html')
@login_required
def reached2000(request):
    users_with_score_2000 = Credit.objects.filter(score__gte=2000).values_list('score', 'user__username')

    # Create an empty dictionary to store the names with scores as keys
    names_dict = {}

    # Add the names and scores to the dictionary
    for score, username in users_with_score_2000:
        names_dict[score] = username

    # Sort the dictionary by keys (scores) in ascending order
    sorted_names = [names_dict[score] for score in sorted(names_dict.keys())]

    context = {
        'sorted_names': sorted_names
    }


    return render(request, 'users/reached2000.html', context)

def reached2000congrats(request):
    score_obj = Credit.objects.get(user=request.user)
    score_obj.reached2000 = True
    score_obj.save()
    return render(request, 'users/reached2000congrats.html')


@login_required
def robbuy(request):
    score_obj = Credit.objects.get(user=request.user)
    ownsrob_status = Credit.objects.filter(ownsrob=True)
    sender_profile = Credit.objects.get(user=request.user)
    ownsrob = {'active_user_pks': [user.user.pk for user in ownsrob_status]}

    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = str(amount)

            if amount and sender_profile.score >= 101:
                sender_profile.score -= 101
                sender_profile.ownsrob = True
                sender_profile.save()



                # Redirect to some success page or show a success message
                return redirect('succ')
            else: return HttpResponseBadRequest(" not enough score to purchase crypto ")
        except ValueError:
            pass

    return render(request, 'users/transfer_score.html')

@login_required
def transfer_score(request, pk):
    score_obj = Credit.objects.get(user=request.user)
    score = score_obj.score
    ownsrob_status = Credit.objects.filter(ownsrob=True)
    sender_profile = Credit.objects.get(user=request.user)
    receiver_profile = get_object_or_404(Credit, user_id=pk)
    ownsrob = {'active_user_pks': [user.user.pk for user in ownsrob_status]}


    try:
        amount = score_obj.invested_score


        #sender_profile.score -= amount

        #sender_profile.save()

        receiver_profile.score += amount
        receiver_profile.ownsrob = False
        receiver_profile.save()

        # Redirect to some success page or show a success message
        return redirect('robbed')
    except ValueError:
        pass

    return render(request, 'users/transfer_score1.html', {'receiver_profile': receiver_profile})

@login_required
def robbed(request):


    return render(request, 'users/robbed.html')

@login_required
def shop(request):
    return render(request, 'users/shop.html')
@login_required
def success(request):
    return render(request, 'users/buysuc.html')

"""
@login_required
def chat(request):
    # Get the Credit model instance for the logged-in user
    user = Credit.objects.get(user=request.user)


    if request.method == 'POST':
        form = Chatform(request.POST)
        if form.is_valid():
            # Get the text from the form
            text = form.cleaned_data['Textbox']
            users = request.user
            users1 = str(users)

            # Update the TextBox field in the Credit model
            if not text.find(">") or not text.find("<"):
                messages.warning(request, "Your text can't contain > or <!")
                user.Textbox += ""

            elif len(text) > 100:
                messages.warning(request, "Text can't be longer than 100 letters")
                user.Textbox += ""
            else:
                user.Textbox += ('\n' +users1 + '  >  ' + text)
            if len(user.Textbox) >= 2000:
                user.Textbox = "Chat cleared"
            if text == '/clear':
                user.Textbox = users1+"  > Cleared chat"


            # Save the updated user object
            user.save()

            # You can redirect to a success page or do other actions if needed
            return redirect('chat')  # Change 'success_page' to your actual URL name

    else:
        form = Chatform()

    context = {
        'textbox': user.Textbox,  # Pass the user's TextBox field to the template
        'form': form,
        # Pass the form to the template
    }

    return render(request, 'users/chat.html', context)
"""
def splitorsteal(request):
    score_obj = Credit.objects.get(user=request.user)
    match_status = Credit.objects.filter(matchready=True)
    ready_pks = [credit.user.pk for credit in match_status]

    if ready_pks and Credit.objects.get(user=request.user).user_id != ready_pks[0]:
        firstready = ready_pks[0]
    else:
        if len(ready_pks) > 1:
            firstready = ready_pks[1]
        else:
            # Handle the case when there are not enough elements in ready_pks
            # You might want to redirect the user to another page or display an error message
            return HttpResponse("Not enough players ready")
    if score_obj.score - 400 >= 0:
        score_obj.score -= 400
        score_obj.save()
    else:
        return HttpResponse("You don't have enough credit to play. PS: atleast 400 or more!")
    context = {'test': match_status}
    score_obj.splitpass = False
    score_obj.save()
    return redirect(f'/splitorstealreal/{firstready}/{Credit.objects.get(user=request.user).user_id}/')


def splitorstealreal(request, pk, pk1):



    receiver_profile = get_object_or_404(Credit, user_id=pk)
    receiver_profile.score -= 400
    receiver_profile.save()
    test = str(Credit.objects.get(user=request.user).user_id)
    mdea = Fight.selected

    test =test.replace("Profile", "")


    score_obj = Credit.objects.get(user=request.user)
    match_status = Credit.objects.filter(matchready=True)
    ready_pks = [credit.user.pk for credit in match_status]

    if ready_pks and Credit.objects.get(user=request.user).user_id != ready_pks[0]:
        firstready = ready_pks[0]
    else:
        if len(ready_pks) > 1:
            firstready = ready_pks[1]
        else:
            # Handle the case when there are not enough elements in ready_pks
            # You might want to redirect the user to another page or display an error message
            return HttpResponse("Not enough players ready")


    if request.method == 'POST':
        response = request.POST.get('response')
        if response == "true":
            value = Fight.objects.first()
            value.Matchfield += f" True {test} " #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #koma et hiljem splittida ja profile saada True.{test}.
            value.save()
            models = Fight.objects.first()
            # You may use .get() or filter to retrieve a specific instance

            # Increment the selected field by 1
            models.selected += 1
            models.secondredir = ""
            models.save()

            return redirect(f'/splitorstealreal/{firstready}/{Credit.objects.get(user=request.user).user_id}/waitingroom')


        else:
            value = Fight.objects.first()
            value.Matchfield += f"False {test} " #tee et see splitib õigesti 4 rühma, mingi probleem on prg!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # koma et hiljem splittida ja profile saadaFalse.{test}.
            value.save()
            models = Fight.objects.first()
              # You may use .get() or filter to retrieve a specific instance

            # Increment the selected field by 1
            models.selected += 1
            models.secondredir = ""
            models.save()
            return redirect(f'/splitorstealreal/{firstready}/{Credit.objects.get(user=request.user).user_id}/waitingroom')

    models = Fight.objects.first()
    splitscores = Splitscores(models.selected)




    context = {
        "text": Fight.objects.first().Matchfield,
        "text1": (Fight.objects.first().selected, type(Fight.objects.first().selected)),
        "text4": Credit.objects.get(user=request.user).splitpass
    }

    return render(request, 'splitorsteal/splitorstealreal.html', context)

# peab lisama mingi uue classi nt trollis sest see aadib True or Faslse ainult useri Textboxi mitte yhisesse
# kui sa juts mindagi neid kasutades välja ei mõtle nt id järgi võttad mõlema resulti ja otsustad
 #ei leia selected yles või ei addi!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Splitscores:
    def __init__(self, selected):
        self.selected = selected
        self.check = False
        if self.selected >= 2:
            self.check = True

    def returner(self):
        return self.check

def splitorstealwait(request,pk, pk1):
    score_obj = Credit.objects.get(user=request.user)
    match_status = Credit.objects.filter(matchready=True)
    ready_pks = [credit.user.pk for credit in match_status]



    if ready_pks and Credit.objects.get(user=request.user).user_id != ready_pks[0]:
        firstready = ready_pks[0]
        secondready = ready_pks[1]
    else:
        if len(ready_pks) > 1:
            firstready = ready_pks[1]
            secondready = ready_pks[0]
        else:
            # Handle the case when there are not enough elements in ready_pks
            # You might want to redirect the user to another page or display an error message
            return HttpResponse("Not enough players ready")

    models = Fight.objects.first()

    splitscores = Splitscores(models.selected)
    myval = False
    score_obj1 = Credit.objects.get(user_id=firstready)
    if splitscores.returner() == True:
        models.secondredir = "True" #tegin str iks sest booleaniga ei töödanud
        models.save()

        #score_obj.splitpass = True
        #score_obj.save()
        #score_obj1 = Credit.objects.get(user_id=firstready)
        #score_obj1.spltpass = True
        #score_obj2 = Credit.objects.get(user_id=secondready)
        #score_obj2.spltpass = True

        #score_obj1.save()
        # Split Matchfield


        instances = Fight.objects.all()
        midagi = Fight.objects.first()

        # Loop through each instance
        for instance in instances:
            # Access the Matchfield attribute
            matchfield_text = midagi.Matchfield

            # Split the Matchfield text into 4 parts

            models.selected = 0
            models.save()

            # but you can adjust the delimiter according to your data

            parti = matchfield_text.split(' ')
            parts = list(filter(None, parti))

            part0 = parts[0]
            part1 = parts[1]
            part2 = parts[2]

            part3 = parts[3]

            models.selected = 0
            models.save()
            models.Matchfield = ""
            models.save()

            user = Credit.objects.get(user_id=part1)
            user1 = Credit.objects.get(user_id=part3)
            if part0 == part2:
                if part0 == "True":

                    user.score += 500

                    user1.score += 500
                    models.messageback = "Users who played: " + user.user.username+ " " + user1.user.username + " and you both splitted"

                    models.save()



                else:
                    models.messageback = "Users who played: " + user.user.username+ " "  + user1.user.username + "and you both stole"
                    models.save()
            elif part0 == "True":

                user.score -= 500
                models.messageback = "Users who played: " + user.user.username+ " "  + user1.user.username + " but"+ " "  + user.user.username + "chose to steal"
                models.save()
            else:

                user1.score += 500
                models.messageback = "Users who played: " + user.user.username+ " "  + user1.user.username + "but"+ " "  + user1.user.username + "chose to steal"
                models.save()
        models.Matchfield = ""
        models.save()

        return redirect(f'/splitorstealreal/{firstready}/{Credit.objects.get(user=request.user).user_id}/final')

    if models.secondredir == "True":
        models.secondredir = ""

        models.save()######ei tööta ######################################################################

        return redirect(f'/splitorstealreal/{firstready}/{Credit.objects.get(user=request.user).user_id}/final')
    context = {
        "text": "Please wait for oppenent answer!",

        "text1": (Fight.objects.first().selected, type(Fight.objects.first().selected)),
        "text3": Fight.objects.first().Matchfield,
        "text4": models.secondredir,


    }

    return render(request, 'splitorsteal/splitorstealwait.html', context)

def splitorstealfinal(request,pk,pk1):
    context = {
        "text": "Results:",
        "text1": (Fight.objects.first().selected, type(Fight.objects.first().selected)),
        "text3": Fight.objects.first().Matchfield,
        "text4": Fight.objects.first().messageback

    }


    return render(request, 'splitorsteal/splitorstealfinal.html', context)


