from django.db import models

class Solution(models.Model):
    question = models.TextField(blank=True)
    # steps = obj.step_set
    cur_chunk = models.IntegerField(default=0)

class Step(models.Model):
    solution = models.ForeignKey(Solution , on_delete=models.CASCADE)
    section = models.IntegerField(default=0)
    text = models.TextField(blank=True)
    is_valid = models.BooleanField(default=True)
    confidence_score = models.FloatField(blank=True)
    explanation = models.TextField(blank=True)
    feedback = models.TextField(blank=True)

