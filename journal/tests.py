# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from journal.models import Resource, Tag
import json
from journal.views import home, new_tip, delete_resource, AJAX_tag_create, TagEdit, TagList
from journal.forms import ResourceForm, TagForm


# Create your tests here.
class TestResources(TestCase):

    def setUp(self):
        tag = Tag.objects.create(name="Django")
        resource = Resource.objects.create(
            name='Facebook',
            link='http://www.facebook.com',
            tip='make friends') # Link the python tag here
        resource.tags.add(tag)
        self.res_id = resource.id
        self.factory = RequestFactory()
        self.tag_post_data = {
            "name":u'Python'
        }
        self.tag_AJAX_data = {
            "tag_name": u'Jenga'
        }
        self.tag_post_data = {
            "tag_name": u'Searching'
        }
        self.resource_post_data = {
            "name": u'Reddit',
            "link": u'http://www.reddit.com',
            "tip": u'use for forums',
            "tags":[unicode(tag.id)],

        }


    def test_resources_show(self):
        request = self.factory.get('/')
        response = home(request)
        self.assertEqual(response.status_code,200)  # Success status
        self.assertContains(response,'Facebook')
        self.assertContains(response,'www.facebook.co')

    def test_resources_create(self):
        request = self.factory.post('/newtip/', self.resource_post_data)
        response = new_tip(request)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Resource.objects.filter(name='Reddit').count(), 1)

    def test_resources_delete(self):
        request = self.factory.post('/deleteresource/' + str(self.res_id))
        response = delete_resource(request, self.res_id)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Resource.objects.filter(name='Facebook').count(),0)

    def test_resources_add_tag(self):   # See whether Python is connected to Facebook after test
        request=self.factory.post('/AJAX_tag_create/', self.tag_AJAX_data)
        response = AJAX_tag_create(request)
        json_string=response.content
        print(json_string)
        data = json.loads(json_string)
        print(data)
        self.assertEqual(data['success'],True)

    def test_tags_show(self):
        request = self.factory.get('/tag_list/')
        response = TagList.as_view()(request)
        self.assertContains(response,'Django')
        self.assertEqual(response.status_code,200)

    # TODO Attach 'python' tag to 'Facebook', filter on python (resources/tag.id), and see if Facebook shows up.
    # def test_resources_filter(self):
    #     request=self.factory.get('/resources/')
    #     response = home(request,tag_id=)

    # def test_resources_link(self):
    #     request = self.factory.get('/') # Not a post or get, how do i do it?

    # def test_tag_create_form(self):
    #     request = self.factory.post('/tag_edit/', self.tag_post_data)
    #     response = TagEdit(request)
    #     self.assertContains(Tag.objects.filter(name='Searching'))



# class TestTagCreateModal(TestCase):


# class TestTagEdit(TestCase):


# class TestTagDelete(TestCase):