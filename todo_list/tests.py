from django.test import TestCase
from todo_list.models import ToDoList, ToDo
from django.contrib.auth.models import User

class TodoListTest(TestCase):
    
    def setUp(self):
        
        self.user1 = User.objects.create_user(username="cyber-jar", password="best-card")
        self.user2 = User.objects.create_user(username="blue-eyes-ultimate-dragon", password="NoNeedPass")
        
        self.list1 = ToDoList.objects.create(name="Empty ToDoList", owner=self.user1)
        self.list2 = ToDoList.objects.create(name="Sunday ToDo List", owner=self.user2)

        ToDo.objects.create(name="Kill dark magician", todoList=self.list2)
        ToDo.objects.create(name="Kill kuriboh", todoList=self.list2)
    
    def test_todo_list_creation(self):
        emptyList = ToDoList.objects.get(name="Empty ToDoList")
        list2 = ToDoList.objects.get(name="Sunday ToDo List")

        self.assertEqual("Empty ToDoList", emptyList.name)
        self.assertEqual(self.user1, emptyList.owner)
        self.assertTrue(len(emptyList.getAllTodo()) == 0)
        
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

        self.assertTrue(len(emptyList.getAllTodo()) == 0)
        self.assertFalse(todo2.isDone)

    def test_mark_done_todo_known(self):
        list2 = ToDoList.objects.get(name="Sunday ToDo List")
        todo2 = ToDo.objects.get(name="Kill kuriboh")

        list2.markDone([todo2.name])

        todo2_updated = ToDo.objects.get(name="Kill kuriboh")
        todo1_updated = ToDo.objects.get(name="Kill dark magician")
        
        self.assertTrue(todo2_updated.isDone)
        self.assertFalse(todo1_updated.isDone)

        # rollback
        todo2_updated.isDone = False
        todo2_updated.save()