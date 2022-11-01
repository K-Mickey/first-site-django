from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .utils import *

class PhotoHome(DataMixin, ListView):
    model = Photo
    template_name = 'photo/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return {**context, **c_def}

    def get_queryset(self):
        return Photo.objects.filter(is_published=True).select_related('cat')


class PhotoCategory(DataMixin, ListView):
    model = Photo
    template_name = 'photo/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Photo.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return {**context, **c_def}


class ShowPost(DataMixin, DetailView):
    model = Photo
    template_name = 'photo/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return {**context, **c_def}


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'photo/addpost.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление поста')
        return {**context, **c_def}

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'photo/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'photo/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'photo/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return {**context, **c_def}

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

def logout_user(request):
    logout(request)
    return redirect("home")

def about(request):
    cats = Category.objects.all()
    return render(request, 'photo/about.html', {'menu': menu, 'title': 'О сайте', 'cats': cats})

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')