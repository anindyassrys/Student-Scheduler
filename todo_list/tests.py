from django.test import TestCase
from todo_list.models import ToDoList, ToDo
from django.contrib.auth.models import User

class TodoListTest(TestCase):
    
    def setUp(self):
        
        user1 = User.objects.create_user(username="cyber-jar", password="best-card")
        user2 = User.objects.create_user(username="blue-eyes-ultimate-dragon", password="NoNeedPass")
        
        list1 = ToDoList.objects.create(name="Empty ToDoList", owner=user1)
        list2 = ToDoList.objects.create(name="Sunday ToDo List", owner=user2)

        ToDo.objects.create(name="Kill dark magician", todoList=list2)
        ToDo.objects.create(name="Kill kuriboh", todoList=list2)
    
    def test_todo_list_creation(self):
        emptyList = ToDoList.objects.get(name="Empty ToDoList")
        list2 = ToDoList.objects.get(name="Sunday ToDo List")

        self.assertEqual("Empty ToDoList", emptyList.name)
        self.assertEqual(self.user1, emptyList.owner)
        self.assertEqual([], emptyList.getAllTodo())

        self.assertEqual("Sunday ToDo List", list2.name)
        self.assertEqual(self.user2, list2.owner)
        self.assertTrue(len(list2.getAllTodo()) > 0)
    
    def test_todo_creation(self):
        todo1 = ToDo.objects.get(name="Kill dark magician")
        
        self.assertEqual("Kill dark magician", todo1.name)
        self.assertEqual(self.list2, todo1.todoList)
        self.assertFalse(todo1.isDone)
    
    def test_mark_done_todo(self):
        todo2 = ToDo.objects.get(name="Kill kuriboh")

        self.assertFalse(todo2.isDone)
        todo2.isDone = True
        self.assertTrue(todo2.isDone)
    
    def test_mark_done_todo_unknown(self):
        emptyList = ToDoList.objects.get(name="Empty ToDoList")
        todo2 = ToDo.objects.get(name="Kill kuriboh")

        emptyList.markDone([todo2.name])

        self.assertEqual([], emptyList.getAllTodo())
        self.assertFalse(todo2.isDone)

    def test_mark_done_todo_known(self):
        list2 = ToDoList.objects.get(name="Sunday ToDo List")
        todo1 = ToDo.objects.get(name="Kill dark magician")
        todo2 = ToDo.objects.get(name="Kill kuriboh")

        list2.markDone([todo2.name])
        self.assertTrue(todo2.isDone)
        self.assertFalse(todo1.isDone)