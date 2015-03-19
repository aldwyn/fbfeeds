from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from login.forms import LoginForm
from django.views import generic


class IndexView(generic.TemplateView):
	template_name = "login/index.html"


def validate(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user:
		if user.is_active:
			login(request, user)
			return render(request, 'login/welcome.html')
		else:
			return render(request, 'login/index.html', {
				'error_message': "Your account has been disabled. It is very much advised that you sign up."
			})
	else:
		return render(request, 'login/index.html', {
			'error_message': "Incorrect username or password."
		})


def logout_view(request):
	logout(request)
	return redirect(reverse('login:index'))