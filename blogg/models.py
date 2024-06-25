from django.db import models

# Create your models here.
class BlogPost(models.Model):
    Post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, default='')
    head1 = models.CharField(max_length=100)
    Chead1 = models.CharField(max_length=5000, null=True, blank=True)
    head2 = models.CharField(max_length=200)
    Chead2 = models.CharField(max_length=5000, null=True, blank=True)
    head3 = models.CharField(max_length=300)
    Chead3 = models.CharField(max_length=5000, null=True, blank=True)
    Pub_Date = models.DateField()
    thumbnail = models.ImageField(upload_to='blogg/images',default="")

    def __str__(self):
        return self.title