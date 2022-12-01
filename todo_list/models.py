from django.db import models
from django.contrib.auth.models import User

class ToDoList(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todoList")
    
    def getAllTodo(self):
        return self.todos.all()

    def markDone(self, todoNames):
        for todoName in todoNames:
            todo = ToDo.objects.get(name=todoName)
            if todo.todoList == self:
                todo.markDone()
                todo.save()

class ToDo(models.Model):
    name = models.CharField(max_length=50)
    isDone = models.BooleanField(default=False)
    todoList = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name="todos")

    def markDone(self):
       self.isDone = True
