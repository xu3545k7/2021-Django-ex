from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
import random
from mysite.models import Post , Country , City
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np

def index(request):
	name = "饒瑞軒"
	lotto = [random.randint(1, 42) for i in range(6)]
	special = lotto[0]
	lotto = lotto[1:6]
	x=np.linspace(-9*np.pi,9*np.pi,360)
	y1 = np.sin(x)
	y2 = np.cos(x)
	plot_div = plot([go.Scatter(x=x, y=y1,
		mode='lines', name='SIN', text="Title",
		opacity=0.8, marker_color='green'),
		go.Scatter(x=x, y=y2,
		mode='lines', name='COS', 
		opacity=0.8, marker_color='blue')],
		output_type='div')
	
	return render(request, "index.html", locals())

def news(request):
	posts = Post.objects.all()
	return render(request, "news.html", locals())
@login_required(login_url="/admin/login/")
def show(request,id):
	try:
		post = Post.objects.get(id=id)
	except:
		redirect("/news/")
	return render(request, "show.html", locals())
@login_required(login_url="/admin/login/")
def rank(request):
	if request.method == 'POST':
		id = request.POST["id"]
		try:
			country=Country.objects.get(id=id)
		except:
			redirect("/rank/")
		cities = City.objects.filter(country=country).order_by('-population')
	else:
		cities=City.objects.all()
	countries= Country.objects.all()
	return render(request, "rank.html", locals())
def chart(request):
	if request.method == 'POST':
		id = request.POST["id"]
		try:
			country=Country.objects.get(id=id)
		except:
			redirect("/chart/")
		cities = City.objects.filter(country=country).order_by('-population')
	else:
		cities=City.objects.all()
	name=[city.name for city in cities]
	population =[city.population for city in cities]
	return render(request, "chart.html", locals())
def mylogout(request):
	logout(request)
	return redirect("/")

def delete(request,id):
	try:
		post = Post.objects.get(id=id)
		post.delete()
	except:
		return redirect("/news/")
	return redirect("/news/")
