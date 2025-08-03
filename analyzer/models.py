from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

class Scenario(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='scenarios', verbose_name="Proyecto")
    title = models.CharField(max_length=255, verbose_name="Título")  # action in infinitive
    goal = models.TextField(verbose_name="Objetivo")
    context = models.TextField(verbose_name="Contexto")
    actors = models.TextField(help_text="Lista separada por comas", verbose_name="Actores")
    resources = models.TextField(help_text="Lista separada por comas", verbose_name="Recursos")
    episodes = models.TextField(help_text="Una acción por línea", verbose_name="Episodios")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Escenario"
        verbose_name_plural = "Escenarios"

class DictionaryTerm(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dictionary_terms', verbose_name="Proyecto")
    term = models.CharField(max_length=100, verbose_name="Término")
    meaning = models.TextField(verbose_name="Significado")
    synonyms = models.TextField(blank=True, help_text="Lista separada por comas", verbose_name="Sinónimos")

    def __str__(self):
        return self.term

    class Meta:
        verbose_name = "Término del diccionario"
        verbose_name_plural = "Términos del diccionario"
