from django.db import models

class Coach(models.Model):
    name = models.CharField(max_length=100)
    license_level = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='coaches/', blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='players/', blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class TrainingSchedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.name} - {self.date}"
