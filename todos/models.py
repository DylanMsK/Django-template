from django.db import models
from core.models import BaseModel


class TodoCategory(BaseModel):
    """Category for Todo. Grouping todos by category."""

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023, blank=True)

    class Meta:
        db_table = "todo_category"

    def __str__(self):
        return self.title


class AbstractTodoModel(BaseModel):
    """Abstract model for Todo and TodoTask."""

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def complete(self):
        self.is_completed = True
        self.save()

    def __str__(self):
        return self.title


class Todo(AbstractTodoModel):
    """Todo that needs to be done. Grouping tasks by todo."""

    category = models.ForeignKey(
        TodoCategory,
        on_delete=models.DO_NOTHING,
        related_name="todos",
        null=True,
    )
    user_id = models.BigIntegerField()

    class Meta:
        db_table = "todo"


class TodoTask(AbstractTodoModel):
    """Task for Todo."""

    todo = models.ForeignKey(
        Todo,
        on_delete=models.DO_NOTHING,
        related_name="tasks",
    )

    class Meta:
        db_table = "todo_task"
