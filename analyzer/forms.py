from django import forms
from .models import Project, Scenario, DictionaryTerm

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            'title', 'goal', 'context', 
            'actors', 'resources', 'episodes'
        ]

class DictionaryTermForm(forms.ModelForm):
    class Meta:
        model = DictionaryTerm
        fields = ['term', 'meaning', 'synonyms']
