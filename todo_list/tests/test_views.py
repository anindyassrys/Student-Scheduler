from django.test import TestCase
from todo_list.views import *
from todo_list.models import *
from django.urls import reverse
import json


class TodoListPopulator(TestCase):
    password = '1X<ISRUkw+tuK'

    def setUp(self):
        self.user1 = Pengguna.objects.create_user(username='testuser1', password=self.password)
        self.user2 = Pengguna.objects.create_user(username="testuser2", password=self.password)

        self.list1 = ToDoList.objects.create(name="list1", owner=self.user1)
        self.list2 = ToDoList.objects.create(name="list2", owner=self.user1)

        self.todo1 = ToDo.objects.create(name="todo1", todoList=self.list1)
        self.todo2 = ToDo.objects.create(name="todo2", todoList=self.list2)


# testing view referance: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#locallibrary_tests

class TestGetTodoListsView(TodoListPopulator):
    
    def test_get_todo_lists_anonymous_user(self):
        response = self.client.get(reverse('todo_lists'))
        self.assertRedirects(response, '/accounts/login/?next=/todo-lists')
    
    def test_get_todo_lists_logged_in_user(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('todo_lists'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'todo_lists.html')
        
        self.assertEqual(2, len(response.context['todo_lists']))

        self.assertEqual(self.list1.name, response.context['todo_lists'][0]['name'])
        self.assertTrue(self.list2.name, response.context['todo_lists'][0]['name'])

class TestGetToDoListDetailView(TodoListPopulator):
    
    def test_detail_todo_list_anonymous_user(self):
        response = self.client.get(reverse('detail_todo_list', args='1'))
        self.assertRedirects(response, '/accounts/login/?next=/todo-list/1')
    
    def test_detail_todo_list_when_todo_list_exists(self):
        self.client.login(username=self.user1.username, password=self.password)
        response = self.client.get(reverse('detail_todo_list', args=str(self.list1.id)))

        self.assertEqual(str(response.context['user']), self.user1.username)
        self.assertEqual(200, response.status_code)

        self.assertEqual(self.list1, response.context['todo_list'])
    
    def test_detail_todo_list_when_doesnt_exist(self):
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.get(reverse('detail_todo_list', args=str(self.list1.id)))

        self.assertEqual(404, response.status_code)

class UpdateToDoList(TodoListPopulator):
    def test_update_todo_list_anonymous_user(self):
        response = self.client.get(reverse('update_todo_list', args='1'))
        self.assertRedirects(response, '/accounts/login/?next=/todo-list/1/update')
    
    def test_update_todo_list_for_eligible_user(self):
        self.client.login(username=self.user1.username, password=self.password)
        response = self.client.post(reverse('update_todo_list', args=str(self.list1.id)), 
                        data=json.dumps({
                            'todos':[self.todo1.id]
                        }),
                        content_type='application/json'
                        )
        todo1 = ToDo.objects.get(id=self.todo1.id)
        todo2 = ToDo.objects.get(id=self.todo2.id)

        self.assertTrue(todo1.isDone)
        self.assertFalse(todo2.isDone)

        self.assertEqual(str(response.context['user']), self.user1.username)
        self.assertEqual(200, response.status_code)
    
    def test_update_todo_list_for_non_existed_todo_list(self):
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.post(reverse('update_todo_list', args=str(self.list1.id)), 
                        data=json.dumps({
                            'todos':[self.todo2.id]
                        }),
                        content_type='application/json'
                        )

        todo2 = ToDo.objects.get(id=self.todo2.id)
        self.assertFalse(todo2.isDone)

        self.assertEqual(404, response.status_code)

class CreateToDoListView(TodoListPopulator):

    def test_create_todo_list_anonymous_user(self):
        response = self.client.get(reverse('create_todo_list'))
        self.assertRedirects(response, '/accounts/login/?next=/todo-lists/create')
    
    def test_get_create_todo_list(self):
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.get(reverse('create_todo_list'))
        self.assertEqual(str(response.context['user']), self.user2.username)
        self.assertEqual(200, response.status_code)

    def test_post_create_todo_list(self):
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.post(reverse('create_todo_list'), 
                data=json.dumps({
                    'list_name':'new_list1',
                    'todo_names': ['todo1', 'todo2']
                }),
                content_type='application/json')
        user2 = Pengguna.objects.get(username=self.user2.username)
        self.assertEqual(1, len(user2.getAllTodoList()))
        self.assertTrue('new_list1', user2.getAllTodoList()[0])

        self.assertEqual(str(response.context['user']), self.user2.username)
        self.assertEqual(200, response.status_code)

class DeleteToDoListView(TodoListPopulator):
    def test_delete_todo_list_anonymous_user(self):
        response = self.client.get(reverse('delete_todo_list', args='1'))
        self.assertRedirects(response, '/accounts/login/?next=/todo-list/1/delete')
    
    def test_delete_existed_todo_list(self):
        self.client.login(username=self.user1.username, password=self.password)
        response = self.client.get(reverse('delete_todo_list', args=str(self.list1.id)))
        
        user1 = Pengguna.objects.get(username=self.user1.username)
        self.assertTrue(len(user1.getAllTodoList()) == 1)

        self.assertEqual(str(response.context['user']), self.user1.username)
        self.assertEqual(200, response.status_code)
    
    def test_delete_not_exist_todo_list(self):
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.get(reverse('delete_todo_list', args=str(self.list2.id)))

        user1 = Pengguna.objects.get(username=self.user1.username)
        self.assertTrue(len(user1.getAllTodoList()) == 2)

        self.assertEqual(404, response.status_code)