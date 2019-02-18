from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from client.forms import PersonForm
from client.models import Person
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

#@login_required - para poder ter acesso a essa minha view somente cquem está
#autenticado na aplicação

@login_required
def persons_list(request):
    #lista todos os clientes
    persons = Person.objects.all()
    return render(request, 'person.html', {'v_persons': persons})

@login_required
def persons_new(request):
    #verifica se já tem algo, se não envia vazio
    #request.FILES - arquivos de midias que estão sendo enviados
    form = PersonForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(persons_list)
    return render(request, 'person_form.html', {'form': form})

@login_required
def persons_update(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect(persons_list)
    return render(request, 'person_form.html', {'form': form})

@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person,  pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if request.method == 'POST':
        person.delete()
        return redirect(persons_list)
    return render(request, 'person_delete_confirm.html', {'person': person, 'form':form})

#se não informar o template_name ele pega o padrão (está em pasta de client)
class PersonList(ListView):
    model = Person
    #definir um template para exibir
    #template_name = 'home3.html'

class PersonDetail(DetailView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
