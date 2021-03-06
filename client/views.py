from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
#Mixis importa métodos para meus cbv
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View

from client.forms import PersonForm
from client.models import Person
from periodos.models import Periodo
from produtos.models import Produto
from vendas.models import Venda
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# ele descubra a url de acordo com o nome
from django.urls import reverse_lazy


# deixar perfomático
# pegar algo específico -  prefetch_related('doc') (sem precisar fazer acesso ao banco
# Person.objects.prefetch_related('doc').all()
# Person.objects.all().values_list('id', 'first_name') = select id, first_name from client_person

# Person.objects.all().order_by('-id') = vir ordem inversa
# Person.objects.all().reverse()

# query vir de forma de dicionario
# from django.forms.models import model_to_dict
# a = Person.objects.all()
# model_to_dict(a)
@login_required
def persons_list(request):
    # lista todos os clientes
    persons = Person.objects.all()
    return render(request, 'person.html', {'v_persons': persons, 'footer_args': 'Tela list'})


@login_required
def persons_new(request):
    if not request.user.has_perm('client.add_person'):
        return HttpResponse('Não autorizado')
    # verifica se já tem algo, se não envia vazio
    # request.FILES - arquivos de midias que estão sendo enviados
    form = PersonForm(request.POST or None, request.FILES or None)

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
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if request.method == 'POST':
        person.delete()
        return redirect(persons_list)
    return render(request, 'person_delete_confirm.html', {'person': person, 'form': form})


# se não informar o template_name ele pega o padrão (está em pasta de client)

#LoginRequiredMixin  - importante vir primeiro do que minha view
#metodos prontos(verifica se está logado
class PersonList(LoginRequiredMixin, ListView):
    model = Person
    # definir um template para exibir
    # template_name = 'home3.html'


class PersonDetail(LoginRequiredMixin, DetailView):
    model = Person

    #sobrescrever método para uma consulta mais perfomática
    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Person.objects.select_related('doc').get(id=pk
                                                        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        vendas = Venda.objects.filter(
            person_id=self.object.id
        )
        context['vendas'] = vendas
        context['count_vendas'] = len(vendas)
        return context


class PersonCreate(LoginRequiredMixin, CreateView):
    model = Person
    # personalizar os fields
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']

    success_url = '/client/person_list'


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = Person
    # personalizar os fields
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    success_url = reverse_lazy('person_list_cbv')


class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Person
    permission_required = ('client.deletar_clientes',)

    # success_url = reverse_lazy('person_list_cbv')
    # outra forma que ficar melhor para manipular
    def get_success_url(self):
        # consigo manipular melhor
        return reverse_lazy('person_list_cbv')


class ProdutoBulk(LoginRequiredMixin, View):
    def get(self, request):
        produtos = ['Banana', 'apple', 'limon', 'orange', 'pineapple']
        list_produtos = []
        for prod in produtos:
            list_produtos.append(Produto(descricao=prod, preco=10))

        Produto.objects.bulk_create(list_produtos)
        return HttpResponse("Salvo com sucesso")




