from django.test import TestCase
from todo_list.models import ToDoList, ToDo, Pengguna

class ObjectCreationSetUp(TestCase):
    def setUp(self):
        user1 = Pengguna(username="cyber-jar", password="best-card")
        user2 = Pengguna(username="blue-eyes-ultimate-dragon", password="NoNeedPass")
        user1.save()
        user2.save()

        self.list1 = ToDoList.objects.create(name="Empty ToDoList", owner=user1)
        self.list2 = ToDoList.objects.create(name="Sunday ToDo List", owner=user2)
        self.list1.save()
        self.list2.save()

        self.todo1 = ToDo(name="Kill dark magician", todoList=self.list2)
        self.todo2 = ToDo(name="Kill kuriboh", todoList=self.list2)
        self.todo1.save()
        self.todo2.save()

class PenggunaTest(ObjectCreationSetUp):
    def test_getAllTodoList(self):
        user1 = Pengguna.objects.get(username="cyber-jar")
        user2 = Pengguna.objects.get(username="blue-eyes-ultimate-dragon")
        self.assertTrue(self.list1 in user1.getAllTodoList())
        self.assertTrue(self.list2 in user2.getAllTodoList())
    
    def test_getTodoList(self):
        
        user1 = Pengguna.objects.get(username="cyber-jar")
        user2 = Pengguna.objects.get(username="blue-eyes-ultimate-dragon")
        self.assertEqual(self.list1, user1.getTodoList(self.list1.id))
        self.assertIsNone(user2.getTodoList(self.list1.id))
    
    def test_createTodoList(self):
        
        user1 = Pengguna.objects.get(username="cyber-jar")

        newTodoList = user1.createTodoList("tdlist2", ["todo1", "todo2"])

        updated_user1 = Pengguna.objects.get(username="cyber-jar")
        self.assertTrue(newTodoList in updated_user1.getAllTodoList())
        
        # rollback
        user1.deleteTodoList(newTodoList.id)
    
    def test_deleteTodoList(self):
        user1 = Pengguna.objects.get(username="cyber-jar")
        newTodoList2 = user1.createTodoList("tdlist3", ["todo3", "todo4"])

        updated_user1 = Pengguna.objects.get(username="cyber-jar")
        self.assertTrue(newTodoList2 in updated_user1.getAllTodoList())

        updated_user1.deleteTodoList(newTodoList2.id)

        updated2_user1 = Pengguna.objects.get(username="cyber-jar")
        self.assertTrue(newTodoList2 not in updated2_user1.getAllTodoList())
        

class TodoTest(ObjectCreationSetUp):

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


class TodoListTest(ObjectCreationSetUp):
    
    def test_todo_list_creation(self):
        user1 = Pengguna.objects.get(username="cyber-jar")
        user2 = Pengguna.objects.get(username="blue-eyes-ultimate-dragon")
        emptyList = ToDoList.objects.get(name="Empty ToDoList")
        list2 = ToDoList.objects.get(name="Sunday ToDo List")

        self.assertEqual("Empty ToDoList", emptyList.name)
        self.assertEqual(user1, emptyList.owner)
        self.assertTrue(len(emptyList.getAllTodo()) == 0)
        
        self.assertEqual("Sunday ToDo List", list2.name)
        self.assertEqual(user2, list2.owner)
        self.assertTrue(len(list2.getAllTodo()) > 0)
    
    def test_mark_done_todo_unknown(self):
        emptyList = ToDoList.objects.get(name="Empty ToDoList")
        todo2 = ToDo.objects.get(name="Kill kuriboh")

        emptyList.markDone([todo2.id])

        updated_emptyList = ToDoList.objects.get(name="Empty ToDoList")
        updated_todo2 = ToDo.objects.get(name="Kill kuriboh")
        self.assertTrue(len(updated_emptyList.getAllTodo()) == 0)
        self.assertFalse(updated_todo2.isDone)

    def test_mark_done_todo_known(self):
        list2 = ToDoList.objects.get(name="Sunday ToDo List")
        todo2 = ToDo.objects.get(name="Kill kuriboh")

        list2.markDone([todo2.id])

        todo2_updated = ToDo.objects.get(name="Kill kuriboh")
        todo1_updated = ToDo.objects.get(name="Kill dark magician")
        
        self.assertTrue(todo2_updated.isDone)
        self.assertFalse(todo1_updated.isDone)

        # rollback
        todo2_updated.isDone = False
        todo2_updated.save()