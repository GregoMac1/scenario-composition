from django.shortcuts import render, get_object_or_404
from .models import Project, DictionaryTerm, Scenario
from .forms import ProjectForm, ScenarioForm, DictionaryTermForm
from django.shortcuts import redirect
from .nlp import lemmatize_episodes, are_sentences_equivalent
from django.utils import timezone
import json

def project_list(request):
    projects = Project.objects.filter(deleted_at__isnull=True)
    return render(request, 'analyzer/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, deleted_at__isnull=True)
    scenarios = project.scenarios.filter(deleted_at__isnull=True)

    for scenario in scenarios:
        if scenario.episodes:
            scenario.episodes_lemmas = lemmatize_episodes(scenario.episodes, project)
        else:
            scenario.episodes_lemmas = []

    return render(request, 'analyzer/project_detail.html', {
        'project': project,
        'scenarios': scenarios
    })

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'analyzer/project_form.html', {'form': form})

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'analyzer/project_form.html', {
        'form': form,
        'project': project
    })

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    if request.method == 'POST':
        project.deleted_at = timezone.now()
        project.save()
        return redirect('project_list')
    return render(request, 'analyzer/delete_confirm.html', {
        'object': project,
        'object_type': 'proyecto',
        'cancel_url': 'project_detail'
    })

def create_scenario(request, project_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)

    if request.method == 'POST':
        form = ScenarioForm(request.POST)
        if form.is_valid():
            scenario = form.save(commit=False)
            scenario.project = project
            scenario.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ScenarioForm()

    return render(request, 'analyzer/scenario_form.html', {
        'form': form,
        'project': project,
        'scenario': None
    })

def edit_scenario(request, project_id, scenario_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    scenario = get_object_or_404(Scenario, pk=scenario_id, project=project, deleted_at__isnull=True)
    if request.method == 'POST':
        form = ScenarioForm(request.POST, instance=scenario)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ScenarioForm(instance=scenario)
    return render(request, 'analyzer/scenario_form.html', {
        'form': form,
        'project': project,
        'scenario': scenario
    })

def delete_scenario(request, project_id, scenario_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    scenario = get_object_or_404(Scenario, pk=scenario_id, project=project, deleted_at__isnull=True)
    if request.method == 'POST':
        scenario.deleted_at = timezone.now()
        scenario.save()
        return redirect('project_detail', pk=project.pk)
    return render(request, 'analyzer/delete_confirm.html', {
        'object': scenario,
        'object_type': 'escenario',
        'cancel_url': 'project_detail'
    })

def dictionary_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    terms = project.dictionary_terms.filter(deleted_at__isnull=True)
    return render(request, 'analyzer/dictionary_list.html', {
        'project': project,
        'terms': terms
    })

def create_dictionary_term(request, project_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    if request.method == 'POST':
        form = DictionaryTermForm(request.POST)
        if form.is_valid():
            term = form.save(commit=False)
            term.project = project
            term.save()
            return redirect('dictionary_list', project_id=project.pk)
    else:
        form = DictionaryTermForm()
    return render(request, 'analyzer/dictionary_form.html', {
        'form': form,
        'project': project
    })

def edit_dictionary_term(request, project_id, term_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    term = get_object_or_404(DictionaryTerm, pk=term_id, project=project, deleted_at__isnull=True)
    if request.method == 'POST':
        form = DictionaryTermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            return redirect('dictionary_list', project_id=project.pk)
    else:
        form = DictionaryTermForm(instance=term)
    return render(request, 'analyzer/dictionary_form.html', {
        'form': form,
        'project': project,
        'term': term
    })

def delete_dictionary_term(request, project_id, term_id):
    project = get_object_or_404(Project, pk=project_id, deleted_at__isnull=True)
    term = get_object_or_404(DictionaryTerm, pk=term_id, project=project, deleted_at__isnull=True)
    if request.method == 'POST':
        term.deleted_at = timezone.now()
        term.save()
        return redirect('dictionary_list', project_id=project.pk)
    return render(request, 'analyzer/delete_confirm.html', {
        'object': term,
        'object_type': 'término del diccionario',
        'cancel_url': 'dictionary_list'
    })

def process_episode(episode, scenarios):
    """
    Process an episode and find semantically similar scenarios.
    Returns a tree structure with the episode name and its children.
    """
    tree = {"name": episode, "children": []}
    
    for scenario in scenarios:
        if are_sentences_equivalent(scenario.title, episode):
            if scenario.episodes:
                sub_episodes = scenario.episodes.strip().split('\n')
                for sub_episode in sub_episodes:
                    if sub_episode.strip():  # Skip empty lines
                        tree["children"].append(process_episode(sub_episode.strip(), scenarios))
    
    return tree

def episode_tree(request, project_id, scenario_id):
    """
    Display the episode tree for a specific scenario.
    Shows how episodes compose into other scenarios.
    """
    project = get_object_or_404(Project, pk=project_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id, project=project)
    
    all_scenarios = project.scenarios.all()
    
    episodes = scenario.episodes.strip().split('\n')
    tree = {
        "name": scenario.title,
        "children": [process_episode(episode.strip(), all_scenarios) for episode in episodes if episode.strip()]
    }

    print(f"Tree: {json.dumps(tree)}")

    return render(request, 'analyzer/episode_tree.html', {
        'project': project,
        'scenario': scenario,
        'tree_data': json.dumps(tree)
    })

def project_episode_composition(request, project_id):
    """
    Display episode composition analysis for all scenarios in a project.
    Shows how episodes from different scenarios compose with each other.
    """
    project = get_object_or_404(Project, pk=project_id)
    scenarios = project.scenarios.all()
    
    composition_analysis = []
    
    for scenario in scenarios:
        if scenario.episodes:
            episodes = scenario.episodes.strip().split('\n')
            episode_compositions = []
            
            for episode in episodes:
                if episode.strip():
                    # Find which other scenarios this episode might compose
                    composing_scenarios = []
                    for other_scenario in scenarios:
                        if other_scenario != scenario and are_sentences_equivalent(other_scenario.title, episode.strip()):
                            composing_scenarios.append(other_scenario.title)
                    
                    episode_compositions.append({
                        'episode': episode.strip(),
                        'composes_into': composing_scenarios
                    })
            
            composition_analysis.append({
                'scenario': scenario,
                'episodes': episode_compositions
            })
    
    return render(request, 'analyzer/project_composition.html', {
        'project': project,
        'composition_analysis': composition_analysis
    })
