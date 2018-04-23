from django.db import models

# Create your models here.


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    client_id = models.CharField(max_length=128, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'session'
