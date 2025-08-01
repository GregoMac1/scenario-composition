#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scenario_composition.settings')
django.setup()

from analyzer.models import Project, DictionaryTerm, Scenario
from analyzer.nlp import analyze_episodes

def test_dictionary_replacement():
    """Test the dictionary replacement functionality"""
    
    # Create a test project
    project, created = Project.objects.get_or_create(
        name="Test Project",
        defaults={'description': 'Test project for dictionary replacement'}
    )
    
    # Create dictionary terms
    term1, _ = DictionaryTerm.objects.get_or_create(
        project=project,
        term="usuario",
        defaults={
            'meaning': "persona que utiliza el sistema",
            'synonyms': "user, cliente"
        }
    )
    
    term2, _ = DictionaryTerm.objects.get_or_create(
        project=project,
        term="sistema",
        defaults={
            'meaning': "aplicación informática",
            'synonyms': "aplicación, software"
        }
    )
    
    # Create a test scenario
    scenario, _ = Scenario.objects.get_or_create(
        project=project,
        title="Test Scenario",
        defaults={
            'goal': 'Test the dictionary replacement',
            'context': 'Testing context',
            'actors': 'usuario, administrador',
            'resources': 'sistema, base de datos',
            'episodes': '''El usuario accede al sistema
El sistema valida las credenciales
El usuario navega por la aplicación'''
        }
    )
    
    print("=== Testing Dictionary Replacement ===")
    print(f"Project: {project.name}")
    print(f"Dictionary terms:")
    for term in project.dictionary_terms.all():
        print(f"  - {term.term} -> {term.meaning} (synonyms: {term.synonyms})")
    
    print(f"\nOriginal episodes:")
    print(scenario.episodes)
    
    print(f"\nAnalyzing episodes...")
    analyzed_episodes = analyze_episodes(scenario.episodes, project)
    
    print(f"\nProcessed episodes:")
    for i, episode in enumerate(analyzed_episodes, 1):
        print(f"  {i}. {episode}")
    
    return analyzed_episodes

if __name__ == "__main__":
    test_dictionary_replacement() 