from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.template import RequestContext
from database.models import *
from django.utils import timezone
import math
from main import forms
# Create your views here.


#############################ACCOUNT##############################

def account_login(request,event_id=None):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user w/db
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Success, check permissions (user/admin)
                if user.is_staff:
                    # Staff redirected to control panel
                    return redirect('/control/')
                else:
                    # User redirected to practice homepage
                    if event_id==None:
                    	return redirect('/home/')
                    else:
                    	return redirect('/event_detial/'+event_id+'/')
                    
            else:
                if user.last_login == user.date_joined:
                    # Not activated
                    return render(request, 'auth.login.html', {'error': 'inactive'})
                else:
                    # User account has been disabled
                    return render_to_response('auth.login.html', {'error': 'disabled'}, context_instance=RequestContext(request))
        else:
            # User account not found or password is incorrect
            return render_to_response('auth.login.html', {'error': 'incorrect'}, context_instance=RequestContext(request))
    else:
        if request.user.is_authenticated():
            if 'next' not in request.GET:
                # Why are you visiting my sign in page again?
                return redirect('/')
            else:
                return render(request, 'auth.login.html', {'error':'permission'})
        else:
            return render(request, 'auth.login.html')


def account_logout(request):
    # Logout for user
    logout(request)

    return render_to_response('auth.logout.html', {}, context_instance=RequestContext(request))

def account_register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST ,request.FILES) # Bind to user submitted form
        if form.is_valid():
            # Process account registration
            user = User.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.userprofile.photo =  form.cleaned_data['photo']
            user.is_active = False
            user.userprofile.save()
            user.save()

            # Generate a activation key using existing salt for pwd
            algorithm, iterations, salt, hashed = user.password.split('$', 3)
            activation_key = make_password(user.email, salt, algorithm)
            algorithm, iterations, salt, activation_key = activation_key.split('$', 3)
            activation_key = activation_key[:-1]
            # Alternative char for + and /
            activation_key = activation_key.replace('+','-').replace('/','_')

            title = 'Account Activation'
            content = render_to_string('register.email', {'first_name': user.first_name, 'last_name': user.last_name, 'is_secure': request.is_secure(), 'host': request.get_host(), 'activation_key': activation_key, 'sender': settings.PROJECT_NAME})

            send_mail(title, content, settings.PROJECT_NAME + ' <' + settings.EMAIL_HOST_USER + '>', [user.email])

            return render(request, 'account.register.success.html')
    else:
        # Display new form for user to fill in
        form = forms.RegistrationForm()

    return render(request, 'account.register.form.html', {'form': form})

def account_activate(request):
    # Already activated
    if request.user.is_authenticated():
        return render(request, 'account.activate.success.html', {'error': 'activated'})

    if request.method == 'GET':
        # Get activation details
        activation_key = request.GET.get('key')

        # No activation key, throw to login page
        if activation_key is None:
            return redirect('/accounts/login/')

        # Keep activation key in session awaiting login
        request.session['activation_key'] = activation_key

        form = forms.ActivationForm()
    else:
        # Attempt to activate user using given user, password and key
        form = forms.ActivationForm(request.POST)
        if form.is_valid():
            # Try logging in
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is None:
                form.activation_error = 'incorrect'
            else:
                # Already active? error!
                if user.is_active:
                    form.activation_error = 'expired'
                else:
                    # Match activation key
                    algorithm, iterations, salt, hashed = user.password.split('$', 3)
                    activation_key = make_password(user.email, salt, algorithm)
                    algorithm, iterations, salt, activation_key = activation_key.split('$', 3)
                    activation_key = activation_key[:-1]
                    # Alternative char for + and /
                    activation_key = activation_key.replace('+','-').replace('/','_')

                    form.key1 = request.session['activation_key']
                    form.key2 = activation_key

                    # Match keys
                    if activation_key == request.session['activation_key']:
                        # Activated, login and proceed
                        user.is_active = True
                        user.save()
                        login(request, user)

                        return render(request, 'account.activate.success.html')
                    else:
                        # Key expired!
                        form.activation_error = 'expired'

    return render(request, 'account.activate.form.html', {'form': form})

def account_forgot(request):
    if request.method == 'POST':
        form = forms.PasswordForgetForm(request.POST) # Bind to user submitted form
        if form.is_valid():
            # Retrieve user from db
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
            except User.DoesNotExist:
                return redirect('/accounts/forgot/?error=nouser')

            # Generate a reset key using existing salt for pwd
            algorithm, iterations, salt, hashed = user.password.split('$', 3)
            reset_key = make_password(user.email, salt, algorithm)
            algorithm, iterations, salt, reset_key = reset_key.split('$', 3)
            reset_key = reset_key[:-1]
            # Alternative char for + and /
            reset_key = reset_key.replace('+','-').replace('/','_')

            title = 'Password Reset'
            content = render_to_string('passwordreset.email', {'first_name': user.first_name, 'last_name': user.last_name, 'host': request.get_host(), 'reset_key': reset_key, 'sender': settings.PROJECT_NAME, 'email': user.email})

            send_mail(title, content, settings.PROJECT_NAME + ' <' + settings.EMAIL_HOST_USER + '>', [user.email])

            return render(request, 'account.forgot.success.html')
    else:
        # Display new form for user to fill in
        form = forms.PasswordForgetForm()

    return render(request, 'account.forget.form.html', {'form': form})

def account_reset(request):
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'GET':
            # TODO: Error messages if key is not valid or email is wrong

            # Reset password for user who has forgotten it
            # Get user from request data
            user_email = request.GET.get('user')

            # Retrieve user from db
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return redirect('/accounts/forgot/?error=nouser')

            # Get reset key from request data
            reset_key_input = request.GET.get('key')

            # No reset key, throw to login page
            if reset_key_input is None:
                return redirect('/accounts/forgot/?error=nokey')

            # Match reset key
            algorithm, iterations, salt, hashed = user.password.split('$', 3)
            reset_key = make_password(user.email, salt, algorithm)
            algorithm, iterations, salt, reset_key = reset_key.split('$', 3)
            reset_key = reset_key[:-1]
            # Alternative char for + and /
            reset_key = reset_key.replace('+','-').replace('/','_')

            # Match keys
            if reset_key == reset_key_input:
                # Reset keys match, render page for user to reset
                # Store reset email in session
                request.session['reset_email'] = user_email

                form = forms.PasswordResetForm(initial={'email': user_email})
            else:
                # Key expired!
                return redirect('/accounts/forgot/?error=keymismatch')
        elif request.method == 'POST':
            form = forms.PasswordResetForm(request.POST)
            if form.is_valid():
                # Perform real resetting of account
                # Check if emails from form and session matches
                if form.cleaned_data['email'] == request.session['reset_email']:
                    # Get user
                    try:
                        user = User.objects.get(email=request.session['reset_email'])
                    except User.DoesNotExist:
                        return redirect('/accounts/forgot/?error=nouser')

                    # Update password of user in system
                    user.set_password(form.cleaned_data['password'])
                    user.save()

                    # Success, login user and display success page
                    user = authenticate(username=user.username, password=form.cleaned_data['password'])
                    login(request, user)

                    return render(request, 'account.reset.success.html')
                else:
                    return redirect('/accounts/forgot/?error=email')

        return render(request, 'account.reset.form.html', {'form': form})


def user_profile(request, user_id):

    user =User.objects.all().get(id=user_id)

    events_id = user.userprofile.future_events.split(';')
    events=[]
    for event_id in events_id:
        if event_id!="":
            events.append(Event.objects.all().get(id=event_id))


    return render(request, 'user_profile.html' , {'events': events})



def user_home(request, page_num=1,sort_id=1):
    "Home view to display practice or trial testing modes"
    if(int(sort_id)==1):
        events = Event.objects.all().order_by('-like')
    if(int(sort_id)==2):
        events = Event.objects.all().order_by('-participant')
    if(int(sort_id)==4):
        events = Event.objects.all().order_by('-organizer')
    if(int(sort_id)==5):
        events = Event.objects.all().order_by('-test')
    if(int(sort_id)==6):
    	events = Event.objects.all().order_by('-pub_date')
    if(int(sort_id)==7):
    	events = Event.objects.all().order_by('d_sort')


    num_of_page = int(math.ceil(float(len(events))/4))
    whole_page=[]
    for i in range(num_of_page):
    	whole_page.append(i+1)

    page_num= int(page_num)

    return render(request, 'home.html' , {'events': events[4*(page_num-1):4*page_num], 'whole_page': whole_page})


@user_passes_test(lambda u: u.is_staff)
def control(request):
    "Control Panel Code"
    # Obtain the list of topics
    return render(request, 'control-pageland.html')


@user_passes_test(lambda u: u.is_staff)
def event_insert(request):
    if request.method == 'POST':
        form = forms.EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = Event(
            title = form.cleaned_data['title'],
            date = str(request.POST['date']),
            organizer= form.cleaned_data['organizer'],
            description = form.cleaned_data['description'],
            content = form.cleaned_data['content'],
            like = 0,
            like_list = '',
            participant = 0,
            p_list = '',
            image =form.cleaned_data['image'],
            test = form.cleaned_data['test'])

            event.save()
            		
            date= event.date.split(" ")
            date[1]=month_match(date[1])
            event.d_sort = int(date[2])*365+ int(date[1])*30+ int(date[0])

            event.save()

            #return redirect('/event/insert/'+ str(event.id))
            return redirect('/control/insert_s/')

    else:
        # Display new form for user to fill in
        form = forms.EventForm(request.POST)

    return render(request, 'event_insert.html')


@user_passes_test(lambda u: u.is_staff)
def event_s(request):

    return render(request, 'insert_s.html')


@user_passes_test(lambda u: u.is_staff)
def event_edit(request, event_id):
    event   = Event.objects.all().get(id=event_id)

    if request.method == 'POST':
        
        form = forms.EventForm(request.POST, request.FILES)

        if form.is_valid():

            event.title = form.cleaned_data['title']
            event.date = str(request.POST['date'])
            event.organizer = str(request.POST['organizer'])
            event.description = form.cleaned_data['description']
            event.content = form.cleaned_data['content']

            date= event.date.split(" ")
            date[1]=month_match(date[1])
            event.d_sort = int(date[2])*365+ int(date[1])*30+ int(date[0])

            



            if form.cleaned_data['image'] !=None:
                event.image =form.cleaned_data['image']
            event.test = form.cleaned_data['test']

            event.save()

            #return redirect('/event/insert/'+ str(event.id))
            return redirect('/control/insert_s/')

    else:
        # Display new form for user to fill in
        form = forms.EventForm(request.POST)


    return render(request, 'event_edit.html', {'event' : event})



@user_passes_test(lambda u: u.is_staff)
def event_management(request):

    events   = Event.objects.all().order_by('pub_date')


    return render(request, 'admin_search.html', {'events': events})


@user_passes_test(lambda u: u.is_staff)
def event_delete(request, event_id):
    d_event = Event.objects.all().get(id=event_id).delete()

    update_events   = Event.objects.all().order_by('pub_date')

    return render(request, 'admin_search.html', {'events': update_events})



def event_detial(request, e_id):

    event = Event.objects.all().get(id = e_id)
    comments = Comment.objects.all().filter(event_id=e_id).order_by('-date')

    like_list = event.like_list.split(';')
    p_list = event.p_list.split(';')

    return render(request, 'event_detial.html', {'event': event, 'comment': comments, 
    	'like_list': like_list, 'p_list': p_list})

def like(request, event_id, user_id=None, user_name=None):
    event = Event.objects.all().get(id = event_id)

    if request.user.is_authenticated():

    	event = Event.objects.all().get(id = event_id)

    	user = User.objects.all().get(id = user_id)

    	user_like_list = user.userprofile.like_events.split(';')

    	for user_event in user_like_list:
    		if user_event == str(event_id):
				# remove user from user_likes

    			user_like_list.remove(event_id)
    			user.userprofile.like_events=""
    			for user_e in user_like_list:
    				if user_e!="":
    					user.userprofile.like_events = user.userprofile.like_events + str(user_e) +";"
    			user.userprofile.save()

    			# remove user from like_list
    			event.like = event.like-1
    			like_list = event.like_list.split(';')
    			like_list.remove(user_name)
    			event.like_list=""
    			for p_user in like_list:
    				if p_user!="":
    					event.like_list = event.like_list + p_user +";"

    			event.save()

    			return redirect('/event_detial/'+event_id+'/')

    	event.like = event.like+1
    	event.like_list = event.like_list+user_name+";"
    	user.userprofile.like_events = user.userprofile.like_events+str(event.id)+";"
    	user.userprofile.save()
    	event.save()

        return redirect('/event_detial/'+event_id+'/')

    return redirect('/event_detial/'+event_id+'/')

def home_like(request, event_id, user_id=None, user_name=None):
    event = Event.objects.all().get(id = event_id)

    if request.user.is_authenticated():

    	event = Event.objects.all().get(id = event_id)

    	user = User.objects.all().get(id = user_id)

    	user_like_list = user.userprofile.like_events.split(';')

    	for user_event in user_like_list:
    		if user_event == str(event_id):
				# remove user from user_likes

    			user_like_list.remove(event_id)
    			user.userprofile.like_events=""
    			for user_e in user_like_list:
    				if user_e!="":
    					user.userprofile.like_events = user.userprofile.like_events + str(user_e) +";"
    			user.userprofile.save()

    			# remove user from like_list
    			event.like = event.like-1
    			like_list = event.like_list.split(';')
    			like_list.remove(user_name)
    			event.like_list=""
    			for p_user in like_list:
    				if p_user!="":
    					event.like_list = event.like_list + p_user +";"

    			event.save()

    			return redirect('/home/')

    	event.like = event.like+1
    	event.like_list = event.like_list+user_name+";"
    	user.userprofile.like_events = user.userprofile.like_events+str(event.id)+";"
    	user.userprofile.save()
    	event.save()

        return redirect('/home/')

    return redirect('/event_detial/'+event_id+'/') 

def paticipate(request, event_id, user_id=None, user_name= None):

    if request.user.is_authenticated():

    	event = Event.objects.all().get(id = event_id)

    	user = User.objects.all().get(id = user_id)

    	user_event_list = user.userprofile.future_events.split(';')

    	for user_event in user_event_list:
    		if user_event == str(event_id):
				# remove user from user_events

    			user_event_list.remove(event_id)
    			user.userprofile.future_events=""
    			for user_e in user_event_list:
    				if user_e!="":
    					user.userprofile.future_events = user.userprofile.future_events + str(user_e) +";"
    			user.userprofile.save()

    			# remove user from paticipant_list
    			event.participant = event.participant-1
    			p_list = event.p_list.split(';')
    			p_list.remove(user_name)
    			event.p_list=""
    			for p_user in p_list:
    				if p_user!="":
    					event.p_list = event.p_list + p_user +";"

    			event.save()

    			return redirect('/event_detial/'+event_id+'/')

    	event.participant = event.participant+1
    	event.p_list = event.p_list+user_name+";"
    	user.userprofile.future_events = user.userprofile.future_events+str(event.id)+";"
    	user.userprofile.save()
    	event.save()

        return redirect('/event_detial/'+event_id+'/')

    else:
        return redirect('/accounts/login/'+event_id+'/')

def home_paticipate(request, event_id, user_id=None, user_name= None):

    if request.user.is_authenticated():

    	event = Event.objects.all().get(id = event_id)

    	user = User.objects.all().get(id = user_id)

    	user_event_list = user.userprofile.future_events.split(';')

    	for user_event in user_event_list:
    		if user_event == str(event_id):
				# remove user from user_events

    			user_event_list.remove(event_id)
    			user.userprofile.future_events=""
    			for user_e in user_event_list:
    				if user_e!="":
    					user.userprofile.future_events = user.userprofile.future_events + str(user_e) +";"
    			user.userprofile.save()

    			# remove user from paticipant_list
    			event.participant = event.participant-1
    			p_list = event.p_list.split(';')
    			p_list.remove(user_name)
    			event.p_list=""
    			for p_user in p_list:
    				if p_user!="":
    					event.p_list = event.p_list + p_user +";"

    			event.save()

    			return redirect('/home/')

    	event.participant = event.participant+1
    	event.p_list = event.p_list+user_name+";"
    	user.userprofile.future_events = user.userprofile.future_events+str(event.id)+";"
    	user.userprofile.save()
    	event.save()

        return redirect('/home/')

    else:
        return redirect('/accounts/login/'+event_id+'/')

def comment(request, event_id, u_name=None, user_id=None):

    if request.user.is_authenticated():

    	if request.method == 'POST':

    		form = forms.CommentForm(request.POST)

    		if form.is_valid():
                
    			comment 	= Comment(
    			event_id 	= event_id,
    			user_name 	= u_name,
    			content 	= form.cleaned_data['content'],
    			user_id		= User.objects.all().get(id=user_id))

    			comment.save()

    			return redirect('/event_detial/'+event_id+'/')

    		else:
    			return redirect('/event_detial/'+event_id+'/')

    	else:
    		form = forms.CommentForm(request.POST)


    else:
        return redirect('/accounts/login/'+event_id+'/#comment')


def comment_delete(request, event_id, comment_id):

	d_event = Comment.objects.all().get(id=comment_id).delete()
	return redirect('/event_detial/'+event_id+'/')

def date_range_search(request):

	if request.method == 'POST':

		start_date = request.POST['start_date']
		end_date = request.POST['end_date']
		date = start_date.split("/")
		date2 = end_date.split("/")
    	events = Event.objects.all().order_by('date')	
    	result = []

    	for event in events:
    		date_list = event.date.split(" ")
    		#date range search
    		if len(date)==3:
    			date_list[1] = int(month_match(date_list[1]))			
    			if int(date_list[2])*365+int(date_list[1])*30+int(date_list[0])>= int(date[2])*365+int(date[1])*30+int(date[0])  and  int(date_list[2])*365+int(date_list[1])*30+int(date_list[0]) <= int(date2[2])*365+int(date2[1])*30+int(date2[0]):
    				result.append(event)

    		if len(date)==2:
    			date_list[1] = int(month_match(date_list[1]))			
    			if  int(date_list[1])*30+int(date_list[0])>= int(date[1])*30+int(date[0])  and  int(date_list[1])*30+int(date_list[0]) <= int(date2[1])*30+int(date2[0]):
    					result.append(event)

    	return render(request, 'home.html' , {'events': result})




def user_search(request):
	if request.method == 'POST':
		tag_input = request.POST['tags']
		date_range = tag_input.split("-")

		if len(date_range)==2:
			date = date_range[0].split("/")
			date2 = date_range[1].split("/")
		else:
			date = tag_input.split("/")			

		tags = tag_input.split(" ")
    	events = Event.objects.all().order_by('date')	
    	result = []
    	for event in events:
    		title = event.title.lower()
    		organizer = event.organizer.lower()
    		test =event.test.lower()

    		for tag in tags:
    			if tag in organizer:
    				result.append(event)
    			if tag in test:
    				result.append(event)
    				break             
    			if tag not in title:
    				break
    			result.append(event)
    			break



    	for event in events:
    		date_list = event.date.split(" ")
    		#date range search
    		if len(date_range)==2:
	    		if len(date)==3:
	    			date_list[1] = int(month_match(date_list[1]))			
	    			if int(date_list[2])*365+int(date_list[1])*30+int(date_list[0])>= int(date[2])*365+int(date[1])*30+int(date[0])  and  int(date_list[2])*365+int(date_list[1])*30+int(date_list[0]) <= int(date2[2])*365+int(date2[1])*30+int(date2[0]):
	    				result.append(event)

	    		if len(date)==2:
	    			date_list[1] = int(month_match(date_list[1]))			
	    			if  int(date_list[1])*30+int(date_list[0])>= int(date[1])*30+int(date[0])  and  int(date_list[1])*30+int(date_list[0]) <= int(date2[1])*30+int(date2[0]):
	    					result.append(event)

    		#date search
    		else:
	    		if len(date)==3:

	    			date_list[1] = int(month_match(date_list[1]))			
	    			if int(date_list[0])== int(date[0]) and int(date_list[1])== int(date[1]) and int(date_list[2])== int(date[2]):
	    				result.append(event)

	    		if len(date)==2:

	    			date_list[1] = int(month_match(date_list[1]))			
	    			if int(date_list[0])== int(date[0]) and int(date_list[1])== int(date[1]):
	    				result.append(event)





    	return render(request, 'home.html' , {'events': result})

@user_passes_test(lambda u: u.is_staff)
def admin_search(request):
	if request.method == 'POST':
		tag_input = str(request.POST['tags'])

		tags = tag_input.split(" ")
    	events = Event.objects.all().order_by('date')	
    	result = []
    	for event in events:
    		title = event.title.lower()
    		for tag in tags:
    			if tag not in title:
    				break
    			result.append(event)
    			break
  		
   	return render(request, 'admin_search.html' , {'events': result})


def month_match(str):
	if(str=="January"):
		return 1
	if(str=="February"):
		return 2
	if(str=="March"):
		return 3
	if(str=="April"):
		return 4
	if(str=="May"):
		return 5
	if(str=="June"):
		return 6
	if(str=="July"):
		return 7
	if(str=="August"):
		return 8
	if(str=="September"):
		return 9
	if(str=="October"):
		return 10
	if(str=="November"):
		return 11
	if(str=="December"):
		return 12

