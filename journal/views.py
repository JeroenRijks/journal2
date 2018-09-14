# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from journal.models import Resource, Tag
from journal.forms import ResourceForm, TagForm, UserForm, LoginForm
from journal.serializers import ResourceSerializer, TagSerializer
from rest_framework import generics
from emoji import emojize


def home(request,tag_id=None):
    resources = Resource.objects.all()
    emoji = emojize(":gorilla:")
    # resources = Resource.objects.filter(created_by=request.user)
    tag = None
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            pass
    if tag:
        resources = resources.filter(tags=tag_id)
    return render(request, 'home.html', {'name': 'Jeroen', 'emoji': emoji, 'items': resources, 'tag': tag})


def tip_edit(request, res_id=None):  # RENAME

    resource = None
    if res_id:
        try:
            resource = Resource.objects.get(id=res_id)
        except Resource.DoesNotExist:
            pass
    tag_form = TagForm()
    if request.method == 'POST':     # This is for the red submit button
        if resource:        # If it exists, edit that instance. Else make a new one.
            form = ResourceForm(data=request.POST, instance=resource)
        else:
            form = ResourceForm(data=request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            if hasattr(request, 'user'):
                if request.user.is_authenticated():
                    if resource:
                        res.last_updated_by = request.user
                    else:
                        res.created_by = request.user
            res.save()
            form.save_m2m()
            return redirect('journal:home')
    else:
        if resource:
            form = ResourceForm(instance=resource)
        else:
            form = ResourceForm()
    return render(request, 'tip_edit.html', {'tagform': tag_form, 'form': form, 'name': 'Jeroen'})


def delete_resource(request, res_id=None):
    if res_id:
        resource = Resource.objects.get(id=res_id)
    else:
        resource = None
    if request.method == 'POST':
        if resource:
            resource.delete()
    return redirect('journal:home')


def AJAX_tag_create(request):
    tag_name = request.POST.get('tag_name', None)
    if tag_name:
            Tag.objects.get_or_create(name=tag_name)        # get_or_create prevents duplication of tags
    full_response = {
    "success": True,
    }

    return JsonResponse(data=full_response, safe=False)


class TagList(View):
    def get(self, request):
        taginfo = Tag.objects.all()
        return render(request, 'tag_list.html', {'name' : 'Jeroen', 'tags' : taginfo})

    def post(self, request,tag_id=None):    # Only post method on this page is a delete function.
        if tag_id:
            tag=Tag.objects.get(id=tag_id)
            tag.delete()
        return redirect('journal:tag_list')


class TagEdit(View):
    def get(self, request, tag_id=None):
        taginfo = None
        if tag_id:
            try:
                taginfo = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                pass
        form_class = TagForm(instance=taginfo)
        return render(request, 'tag_edit.html', {'tag': taginfo, 'form': form_class})

    def post(self, request, tag_id=None):
        taginfo = None
        if tag_id:     # Edit or create
            try:
                taginfo = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                pass
        form_class = TagForm(request.POST, instance=taginfo)
        if form_class.is_valid():
            form_class.save()

        return redirect('journal:tag_list')


# APIs

class ResourceListCreate(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# Trying to make an api that can select by tag id
# class ResourceListSelect(generics.ListCreateAPIView, tag_id=None):
#     queryset = Resource.objects.all()
#     if tag_id:
#         try:
#             queryset = Resource.objects.get(id=tag_id)
#         except Tag.DoesNotExist:
#             pass
#     serializer_class = ResourceSerializer

# User Authentication


class UserView(View):
    form_class = UserForm
    form = None
    user = None
    username = None
    password = None
    action = 'empty string'

    # display empty form
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, 'register.html', {'form': form, 'action': self.action})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.username = form.cleaned_data['username']
            self.password = form.cleaned_data['password']
            self.form = form

    def auth_login(self, request):
        user = authenticate(username=self.username, password=self.password)
        if user is not None:
            if user.is_active:
                login(request, user)


class Login(UserView):
    form_class = LoginForm
    action = 'Login'

    def get(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            return redirect('journal:home')
        return super(Login, self).get(request)

    def post(self, request):
        super(Login, self).post(request)
        self.auth_login(request)
        return redirect('journal:home')


class Register(UserView):

    action = 'Register'

    # process form data
    def post(self, request):
        super(Register, self).post(request)

        user = self.form.save(commit=False) if self.form else None
        if user:
            user.set_password(self.password)
            user.save()
            self.auth_login(request)
        return redirect('journal:home')


def logoutview(request):
    if hasattr(request, 'user'):
        logout(request)
    return redirect('journal:home')
