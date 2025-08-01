from django.shortcuts import render, get_object_or_404
from .models import Project, DictionaryTerm, Scenario
from .forms import ProjectForm, ScenarioForm, DictionaryTermForm
from django.shortcuts import redirect
from .nlp import lemmatize_episodes

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'analyzer/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    scenarios = project.scenarios.all()

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

def create_scenario(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

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
    project = get_object_or_404(Project, pk=project_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id, project=project)
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

def dictionary_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    terms = project.dictionary_terms.all()
    return render(request, 'analyzer/dictionary_list.html', {
        'project': project,
        'terms': terms
    })

def create_dictionary_term(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
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
    project = get_object_or_404(Project, pk=project_id)
    term = get_object_or_404(DictionaryTerm, pk=term_id, project=project)
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
