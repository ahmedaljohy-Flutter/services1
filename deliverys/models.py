from django.db import models
from django.contrib.auth.models import User

class Delivery(models.Model):
    delv_name = models.CharField(max_length=100)
    description = models.TextField()
    delivered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.delv_name