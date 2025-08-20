from django.db import models

class SessionComparison(models.Model):
    session_id_1 = models.CharField(max_length=255)
    session_id_2 = models.CharField(max_length=255)
    preferred = models.IntegerField()

    def __str__(self):
        return f"{self.session_id_1} vs {self.session_id_2} -> Preferred: {self.preferred}"

class Session(models.Model):
    name = models.CharField(max_length=255, unique=True)
    data = models.JSONField(null=True) # Add this field

    def __str__(self):
        return self.name
