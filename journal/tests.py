# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory, Client
from journal.models import Resource, Tag
from django.contrib.auth.models import User
import json
from journal.views import *
from journal.forms import ResourceForm, TagForm
from django.urls import reverse, resolve

# Create your tests here.


class TestObjects(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        # Create data
        tag = Tag.objects.create(
            name="Django"
        )
        resource = Resource.objects.create(
            name='Facebook',
            link='http://www.facebook.com',
            tip='make friends'
        )
        Resource.objects.create(
            name='Google',
            link='http://www.google.com',
            tip='make searches'
        )

        resource.tags.add(tag)  # Add Django tag to Facebook resource
        self.res_id = resource.id
        self.tag_id = tag.id

        # Post data
        self.tag_post_data = {
            "name": u'Python'
        }
        self.tag_edit_post_data = {
            "name": u'Javascript'
        }
        self.tag_AJAX_data = {
            "tag_name": u'Jenga'
        }
        self.resource_post_data = {
            "name": u'Reddit',
            "link": u'http://www.reddit.com',
            "tip": u'use for forums',
            "tags": [unicode(tag.id)],
        }

    def test_resources_create(self):
        request = self.factory.post('/newtip/', self.resource_post_data)
        response = tip_edit(request)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Resource.objects.filter(name='Reddit').count(), 1)

    def test_resources_show(self):
        request = self.factory.get('/')
        response = home(request)
        self.assertEqual(response.status_code, 200)  # Success status
        self.assertContains(response, 'Facebook')
        self.assertContains(response, 'www.google.com')

    def test_resources_delete(self):
        request = self.factory.post('/deleteresource/' + str(self.res_id))
        response = delete_resource(request, self.res_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Resource.objects.filter(name='Facebook').count(), 0)

    def test_AJAX_add_tag(self):   # See whether Python is connected to Facebook after test
        request=self.factory.post('/AJAX_tag_create/', self.tag_AJAX_data)
        response = AJAX_tag_create(request)
        json_string=response.content
        data = json.loads(json_string)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_tags_show(self):
        request = self.factory.get('/tag_list/')
        response = TagList.as_view()(request)
        self.assertContains(response, 'Django')
        self.assertEqual(response.status_code, 200)

    def test_resources_filter(self):
        request = self.factory.get('/' + str(self.tag_id))
        response = home(request, self.tag_id)
        self.assertContains(response, 'Django')
        self.assertContains(response, 'Facebook')
        self.assertNotContains(response, 'Google')
        self.assertEqual(response.status_code, 200)

    def test_create_tag_form(self):
        request = self.factory.post('/tag_edit/', self.tag_post_data)
        response = TagEdit.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.filter(name='Python').count(), 1)

    def test_edit_tag(self):
        request = self.factory.post('tag_edit' + str(self.tag_id), self.tag_edit_post_data)
        response = TagEdit.as_view()(request, tag_id=self.tag_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.filter(name='Django').count(), 0)
        self.assertEqual(Tag.objects.filter(name='Javascript').count(), 1)

    def test_delete_tag(self):
        request = self.factory.post('/deletetag/' + str(self.tag_id))
        response = TagList.as_view()(request, tag_id=self.tag_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.filter(name='Django').count(), 0)


class TestLogin(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {
            'username': u'unlogged_user',
            'email': u'unlogged_user@unlogged_user.com',
            'password': u'password',
        }
        User.objects.create_user(self.credentials)

    def test_login(self):  #
        request = self.factory.post('/login/', self.credentials)
        response = Login.as_view()(request)
        response.client = Client()
        self.assertRedirects(response, '/resources/')
        self.assertEqual(response.status_code, 302)


class TestRegister(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {
            'username': u'new_user',
            'email': u'new_user@new_user.com',
            'password': u'password',
        }

    def test_register(self):
        request = self.factory.post('/register/', self.credentials)
        response = Register.as_view()(request)
        response.client = Client()
        self.assertRedirects(response, '/resources/')
        self.assertEqual(response.status_code, 302)


class TestLoggedIn(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.credentials = {
            'username': u'new_user',
            'email': u'new_user@new_user.com',
            'password': u'password',
        }
        User.objects.create_user(self.credentials)
        Client().login(username='new_user', password='password')

    def test_logged_in_homepage(self):
        request = self.factory.get('/')
        response = home(request)
        self.assertContains(response, 'new')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        request = self.factory.get('/logout/')
        response = logoutview(request)
        response.client = Client()
        self.assertRedirects(response, '/resources/')
        self.assertEqual(response.status_code, 302)