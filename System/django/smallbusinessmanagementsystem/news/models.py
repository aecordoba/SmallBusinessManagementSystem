from django.db import models
from django.urls import reverse
from accounting.models import Event


class News(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event', blank=True, null=True)
    creation = models.DateTimeField()
    brief = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.creation) + ' - ' + self.brief

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

    class Meta:
        managed = False
        db_table = 'news'
        ordering = ['-creation']
        verbose_name = 'News'
        verbose_name_plural = 'News'
