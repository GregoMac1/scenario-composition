from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Scenario(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='scenarios')
    title = models.CharField(max_length=255)  # action in infinitive
    goal = models.TextField()
    context = models.TextField()
    actors = models.TextField(help_text="Comma-separated list")
    resources = models.TextField(help_text="Comma-separated list")
    episodes = models.TextField(help_text="One action per line")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DictionaryTerm(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dictionary_terms')
    term = models.CharField(max_length=100)
    meaning = models.TextField()
    synonyms = models.TextField(blank=True, help_text="Comma-separated list")

    def __str__(self):
        return self.term
