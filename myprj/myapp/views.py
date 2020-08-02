from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import *
from .forms import SignupForm, LoginForm, PasswordForm
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.contrib import messages
import base64
# Create your views here.

def signup(request):
	""" Signup. Stores user info to MongoDB after data is validated on both client and server side.
	Set session info and flash message on success. Raise appropriate errors otherwise. """

	# Flush expired session info
	request.session.clear_expired()

	# Display empty form if no request or 'GET' request. Accept data if 'POST' request.
	if request.method == 'POST':
		filled_form = SignupForm(request.POST, request.FILES)
		if filled_form.is_valid() and filled_form.cleaned_data['password'] == filled_form.cleaned_data['confirm_password']: 
			# Create new object
			created_user = User(
				name = filled_form.cleaned_data['name'],
				email = filled_form.cleaned_data['email'],
				phoneno = filled_form.cleaned_data['phoneno'],
				passport = filled_form.cleaned_data['passport'],
				birth_date = filled_form.cleaned_data['birth_date'],
				passwd = make_password(filled_form.cleaned_data['confirm_password']),
				img = filled_form.cleaned_data['img'],
			)
			created_user.last_sign_in = datetime.now()
			created_user.save()
			messages.success(request, 'Registration successful! Please proceed to login.')

			filled_form =  SignupForm()
		else:
			messages.warning(request, "Invalid details or confirm password mismatch. Try again.")
		return render(request, 'signup.html', {'signupform':filled_form,})
	else:
		form = SignupForm()
		return render(request, 'signup.html', {'signupform':form,})

def login(request):
	""" Login. Authenticate if username is in database and password matches user's password. 
	Set session info and Redirect to user's dashboard if successful. 
	Raise appropriate errors otherwise. """

	# Flush expired session info
	request.session.clear_expired()

	print("Inside login")  # For debugging purposes

	# Check for active sessions. Redirect to dashboard if active session found.
	if "userid" in request.session and request.session.get_expiry_age():
		print("login : ", request.session['userid'])   # For debugging purposes
		usr = get_object_or_404(klass=User, id=request.session['userid'])
		return redirect(usr.get_absolute_url() , permanent=True)

	# Display login form if no request or 'GET' request. 
	# Accept data and authenticate user on 'POST' request.
	if request.method == 'POST':
		
		filled_form = LoginForm(request.POST)
		if filled_form.is_valid():

			try:
				usr = User.objects.get(phoneno=filled_form.cleaned_data['phoneno'])
				if check_password(filled_form.cleaned_data['password'], usr.passwd):
					
					# Set last sign in to Now.
					usr.last_sign_in = datetime.now()
					usr.save(update_fields=['last_sign_in'])

					# Set session info using request object and redirect to dashboard.
					request.session["userid"] = str(usr.id)
					request.session.set_expiry(360)
					return redirect(usr.get_absolute_url() , permanent=True)
				else:
					messages.error(request, 'Wrong password. Try again!')
			except:
				messages.error(request, 'User not Registered.')
		else:
			messages.warning(request, 'Invalid details. Try again.')
		return render(request, 'login.html', {'loginform':filled_form,})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'loginform':form,})

def dashboard(request):
	""" Dashboard. Check session info. If session is active, gather and display user info.
	Raise appropriate errors if no session is active or session expired. """
	
	# Flush expired session info
	request.session.clear_expired()

	# Check for an active session on the request object
	if "userid" in request.session: #and request.session.get_expiry_age():
		print("dashboard : ", request.session.get_expiry_age())  # For debugging purposes
		print("dashboard : ", request.session['userid'])  # For debugging purposes

		usrid = request.session["userid"]
		usr = get_object_or_404(klass=User, id=usrid)	# Get user object from session info
		i = usr.img.read()								# Read image as bytes
		i = base64.b64encode(i).decode('utf-8')			# Encode bytes to send as response
		img = 'data:image/%s;base64,%s' % (usr.img.format.lower(), i)
		name = usr.name									# Get user info
		email = usr.email
		birth_date = usr.birth_date
		passport = usr.passport
		phoneno = usr.phoneno
		return render(request, 'dashboard.html', {'name':name, 'email':email, 'birth_date': birth_date, 'passport':passport, 'img':img, 'phoneno':phoneno})
	else:
		raise Http404("No session is active [OR] Active session expired. Please visit the login page.")


def change_passwd(request):
	""" Change password. If session is valid and old password matches with the user's password data,
	update the password info in users record. Raise appropriate errors otherwise. """

	# Flush expired session info
	request.session.clear_expired()

	# Check if session is active on request object.
	if "userid" in request.session and request.session.get_expiry_age():
		usrid = request.session["userid"]
		usr = get_object_or_404(klass=User, id=usrid)

		# Display Change Password form if no request or 'GET' request. Accept data if 'POST' request.
		if request.method == 'POST':
			filled_form = PasswordForm(request.POST)
			if filled_form.is_valid():
				if check_password(filled_form.cleaned_data['old_password'], usr.passwd) and filled_form.cleaned_data['new_password'] == filled_form.cleaned_data['confirm_new_password']:
					
					# Make password hash and store it in user's record in database.
					usr.passwd = make_password(filled_form.cleaned_data['confirm_new_password'])
					usr.save()
					messages.success(request, 'Change password successful! Please visit login page.')

					# Set session expiry.  
					request.session.set_expiry(10)
				else:
					messages.error(request, 'Old password does not match [OR] Confirm password mismatch.')
			else:
				messages.warning(request, 'Invalid details. Try again.')
			return render(request, 'change_passwd.html', {'change_passwd':filled_form,})

		else:
			form = PasswordForm()
			return render(request, 'change_passwd.html', {'change_passwd':form, 'name':usr.name})
	else:
		raise Http404("No session is active [OR] Active session expired. Please visit the login page.")


def logout(request):
	""" Logout. Check for an active session on request object and flush its info from database.
	Raise appropriate errors otherwise. """

	# Flush expired session info
	request.session.clear_expired()

	# Check for active session.
	if "userid" in request.session and request.session.get_expiry_age():
		print("Inside logout")  # For debugging purposes
		print("Logout : ", request.session["userid"])  # For debugging purposes

		# Flush the session info.
		try:
			request.session.flush()
		except Exception as e:
			raise e	
		return redirect('login' , permanent=True)
	else:
		raise Http404("No session is active [OR] Active session expired. Please visit the login page.")


