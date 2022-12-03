from django.test import TestCase
from todo_list.views import *
from todo_list.models import *
from django.urls import reverse
import json

class TodoListPopulator(TestCase):
    
    def setUp(self):
        self.user1 = Pengguna.objects.create_user(username="a", password="bcd")
        self.user2 = Pengguna.objects.create_user(username="b", password="def")

        self.list1 = ToDoList.objects.create(name="list1", owner=self.user1)
        self.list2 = ToDoList.objects.create(name="list2", owner=self.user1)

        self.todo1 = ToDo.objects.create(name="todo1", todoList=self.list1)
        self.todo2 = ToDo.objects.create(name="todo2", todoList=self.list2)


# testing view referance: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#locallibrary_tests

class TestGetTodoListsView(TodoListPopulator):
    
    def test_view_anonymous_user(self):
        response = self.client.get(reverse('todo_lists'))
        self.assertRedirects(response, reverse('home'))
    
    def test_view_logged_in_user(self):
        self.client.login(username=self.user1.get_username, password="bcd")
        response = self.client.get(reverse('todo_lists'))

        self.assertEqual(str(response.context['user']), 'a')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'todo_list/todo_lists.html')
        
        self.assertEqual(2, len(response.context['todo_lists']))
        self.assertTrue(self.list1 in response.context['todo_lists'])
        self.assertTrue(self.list2 in response.context['todo_lists'])

class TestGetToDoListDetailView(TodoListPopulator):
    
    def test_view_anonymous_user(self):
        response = self.client.get(reverse('detail_todo_list', args=self.list1.id))
        self.assertRedirects(response, reverse('home'))
    
    def test_view_todo_list_exists(self):
        self.client.login(username=self.user1.get_username, password="bcd")
        response = self.client.get(reverse('detail_todo_list', args=self.list1.id))

        self.assertEqual(str(response.context['user']), 'a')
        self.assertEqual(200, response.status_code)

        self.assertEqual(self.list1, response.context['todo_list'])
    
    def test_view_todo_list_doesnt_exist(self):
        self.client.login(username=self.user2.get_username, password="def")
        response = self.client.get(reverse('detail_todo_list', args=self.list1.id))

        self.assertEqual(str(response.context['user']), 'b')
        self.assertEqual(404, response.status_code)

class UpdateToDoList(TodoListPopulator):
    def test_view_anonymous_user(self):
        response = self.client.get(reverse('update_todo_list', args=self.list1.id))
        self.assertRedirects(response, reverse('home'))
    
    def test_update_todo_list_for_eligible_user(self):
        self.client.login(username=self.user1.get_username, password="bcd")
        response = self.client.post(reverse('update_todo_list', args=self.list1.id), 
                        data=json.dumps({
                            'todos':[self.list1.id]
                        }))
        
        todo1 = ToDo.objects.get(id=self.todo1.id)
        todo2 = ToDo.objects.get(id=self.todo2.id)

        self.assertTrue(todo1.isDone)
        self.assertFalse(todo2.isDone)

        self.assertEqual(str(response.context['user']), 'a')
        self.assertEqual(200, response.status_code)
    
    def test_update_todo_list_for_illegal_user(self):
        self.client.login(username=self.user2.get_username, password="def")
        response = self.client.post(reverse('update_todo_list', args=self.list1.id), 
                        data=json.dumps({
                            'todos':[self.list2.id]
                        }))

        todo2 = ToDo.objects.get(id=self.todo2.id)
        self.assertFalse(todo2.isDone)

        self.assertEqual(str(response.context['user']), 'b')
        self.assertEqual(403, response.status_code)

class CreateToDoListView(TestCase):
    def setUp(self):
        self.user1 = Pengguna.objects.create_user(username="a", password="bcd")
        self.user2 = Pengguna.objects.create_user(username="b", password="def")

    def test_view_anonymous_user(self):
        response = self.client.get(reverse('create_todo_list'))
        self.assertRedirects(response, reverse('home'))
    
    def test_create_todo_list(self):
        self.client.login(username=self.user1.get_username, password="bcd")
        response = self.client.post(reverse('create_todo_list'), 
                data=json.dump({
                    'list_name':'new_list1',
                    'todo_names': ['todo1', 'todo2']
                }))
        user1 = Pengguna.objects.get(username='a')
        self.assertEqual(1, len(user1.getAllTodoList()))
        self.assertTrue('new_list1', user1.getAllTodoList()[0])

        self.assertEqual(str(response.context['user']), 'a')
        self.assertEqual(200, response.status_code)

class DeleteToDoListView(TodoListPopulator):
    def test_view_anonymous_user(self):
        response = self.client.get(reverse('delete_todo_list'))
        self.assertRedirects(response, reverse('home'))
    
    def test_delete_todo_list_for_eligible_user(self):
        self.client.login(username=self.user1.get_username, password="bcd")
        response = self.client.post(reverse('delete_todo_list', args=self.list1.id))
        
        user1 = Pengguna.objects.get(username='a')
        self.assertTrue(self.list1 not in user1.getAllTodoList())
        self.assertTrue(self.list2 in user1.getAllTodoList())

        self.assertEqual(str(response.context['user']), 'a')
        self.assertEqual(200, response.status_code)
    
    def test_delete_not_exist_todo_list(self):
        self.client.login(username=self.user2.get_username, password="def")
        response = self.client.post(reverse('delete_todo_list', args=self.list2.id))

        user1 = Pengguna.objects.get(username='a')
        self.assertTrue(self.list2 in user1.getAllTodoList())

        self.assertEqual(str(response.context['user']), 'b')
        self.assertEqual(404, response.status_code)