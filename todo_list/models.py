from django.db import models
from django.contrib.auth.models import User

class ToDoList(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todoList")
    
    def getAllTodo(self):
        return self.todos.all()

    def markDone(self, todoIds):
        for todo in self.todos.all():
            if todo.id in todoIds:
                todo.markDone()
            else:
                todo.isDone=False
            todo.save()

class ToDo(models.Model):
    name = models.CharField(max_length=50)
    isDone = models.BooleanField(default=False)
    todoList = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name="todos")

    def markDone(self):
       self.isDone = True

class Pengguna(User):
    class Meta:
        proxy = True
    
    def getAllTodoList(self):
        return self.todoList.all()
    
    def getTodoList(self, todoListId):
        try:
            return self.todoList.filter(id=todoListId).get()
        except:
            return None
    
    def deleteTodoList(self, todoListId):
        todoList = self.todoList.filter(id=todoListId).delete()
        return todoList
    
    def createTodoList(self, todoListName, todos):
        todoList = ToDoList.objects.create(name=todoListName, owner=self)
        for todo in todos:
            ToDo.objects.create(name=todo, todoList=todoList).save()
        todoList.save()
        return todoList