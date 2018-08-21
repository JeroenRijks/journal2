# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from journal.models import Resource, Tag
from journal.forms import ResourceForm, TagForm, UserForm
from journal.serializers import ResourceSerializer, TagSerializer
from rest_framework import generics


def home(request,tag_id=None):
    resources = Resource.objects.all()
    tag = None
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            pass
    if tag:
        resources = resources.filter(tags=tag_id)
    return render(request, 'home.html', {'name': 'Jeroen', 'items': resources, 'tag': tag})


def new_tip(request, res_id=None):
    if res_id:
        try:
            resource = Resource.objects.get(id=res_id)
        except Resource.DoesNotExist:
            resource = None
    else:
        resource = None
    tag_form = TagForm()

    if request.method == 'POST':     # This is for the red submit button
        if resource:        # If it exists, edit that instance. Else make a new one.
            form = ResourceForm(data=request.POST, instance=resource)
        else:
            form = ResourceForm(data=request.POST)
        if form.is_valid():
            form.save()
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

    print(JsonResponse(data=full_response, safe=False))
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
                taginfo = None
                form_class = TagForm(instance = taginfo) # lil change
        else:
            taginfo = None
            form_class = TagForm(instance = taginfo)
        return render(request, 'tag_edit.html', {'tag': taginfo, 'tag_form' : form_class})

    def post(self, request, tag_id=None):
        if tag_id:     # Edit or create
            try:
                taginfo = Tag.objects.get(id=tag_id)
                form_class = TagForm(request.POST, instance = taginfo)
            except Tag.DoesNotExist:
                form_class = TagForm(request.POST)
        else:
            form_class = TagForm(request.POST)
        if form_class.is_valid():
            form_class.save()

        return redirect('journal:tag_list')


class ResourceListCreate(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class Register(View):
    form_class = UserForm

    # display empty form
    def get(self, request):
        form = self.form_class(None)
        return render(request, 'register.html', {'form' : form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'journal:home', {'name': 'Jeroen'})

        return render(request, 'register.html', {'name' : 'Jeroen'})