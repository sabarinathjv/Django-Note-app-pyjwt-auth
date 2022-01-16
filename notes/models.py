from django.db import models
from django.contrib.auth.models import User



def upload_to(instance, filename):
    return f'posts/{filename}' 



class Note(models.Model):

    title = models.CharField(max_length=250)
    notes = models.TextField()
    image = models.ImageField("Image", upload_to=upload_to, default='posts/default.jpg')
    user = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE)
    updated_on = models.DateTimeField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

   


    def __str__(self):
        return self.title  