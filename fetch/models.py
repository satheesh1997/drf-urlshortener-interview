from django.db import models

class Shorturl(models.Model):
    created   = models.DateTimeField(auto_now_add=True)
    long_url  = models.URLField()
    short_url = models.CharField(max_length=8)
    count     = models.IntegerField(default=0)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.long_url