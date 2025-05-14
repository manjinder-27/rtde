from django.db import models
from django.contrib.auth.models import User
import string ,secrets


def generate_unique_id(length=16):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(secrets.choice(characters) for _ in range(length))

class Document(models.Model):
    id = models.BigAutoField(primary_key=True)
    uniqID = models.CharField(max_length=16)
    name = models.CharField(max_length=30)
    content = models.TextField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def assignUniqID(self):
        while True:
            new_id = generate_unique_id()
            if not Document.objects.filter(uniqID=new_id).exists():
                self.uniqID = new_id
                break
    
    def save(self, *args, **kwargs):
        if not self.uniqID:
            self.assignUniqID()
        super().save(*args, **kwargs)