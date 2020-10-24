from django.db import models
from django.contrib.auth.models import User
from datetime import date
from simple_history.models import HistoricalRecords

# Create your models here.
class Book(models.Model):
    """Model representing a book that can be borrowed from the library."""
    number = models.CharField(max_length=9,
                          help_text="Year/number: YYYY/num", unique=True)
    name = models.CharField(max_length=200)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    borrowed_on = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(blank=True, default=True, help_text='Dostępność książki')
    history = HistoricalRecords()
    created = models.DateField(null=True, blank=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.number, self.name)