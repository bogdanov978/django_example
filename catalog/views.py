import re

from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ChangeBookinstanceForm, AddBookinstanceForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
import datetime

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
    # количество жанров
    num_genres=Genre.objects.count()
    # количество посещений страницы
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request, 'index.html', context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_genres':num_genres, 'num_visits':num_visits}
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #context_object_name = 'my_book_list'   # ваше собственное имя переменной контекста в шаблоне
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Получение 5 книг, содержащих слово 'war' в заголовке
    #template_name = 'books/my_arbitrary_template_name_list.html'  # Определение имени вашего шаблона и его расположения


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class GenreListView(generic.ListView):
    model = Genre


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ['catalog.add_bookinstance', 'catalog.change_bookinstance', 'catalog.delete_bookinstance',]
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


#  отображения форм для модели Author:
class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_author'
    model = Author
    fields = '__all__'
    #initial={'date_of_birth':'12/10/1976',} # пример задания начального значения поля


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_author'
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_author'
    model = Author
    success_url = reverse_lazy('authors')


#  отображения форм для модели Book:
class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_book'
    model = Book
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_book'
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_book'
    model = Book
    success_url = reverse_lazy('books')


#  отображения форм для модели Genre:
class GenreCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_genre'
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('genres')


class GenreUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_genre'
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('genres')


class GenreDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_genre'
    model = Genre
    success_url = reverse_lazy('genres')


#  отображение для формы, создающей экземпляры Bookinstance
@permission_required('catalog.add_bookinstance')
def add_bookinstance(request, pk):
    book = get_object_or_404(Book, pk=pk)
    maintenance_end = datetime.date.today() + datetime.timedelta(days=3)
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        #  Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = AddBookinstanceForm(request.POST)
        #  Проверка валидности данных формы:
        if form.is_valid():
            book_inst = BookInstance()
            book_inst.book = book
            book_inst.imprint = form.cleaned_data['imprint']
            book_inst.due_back = maintenance_end
            book_inst.status = 'm'
            book_inst.borrower = None
            book_inst.save()

            return HttpResponseRedirect(reverse('book-detail', args = [book.pk]))

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        form = AddBookinstanceForm()

    return render(request, 'catalog/bookinstance_add.html', {'form': form, 'title': book.title, 'maintenance_end': maintenance_end},)


# отображение для формы, управляющей выдачей книг
@permission_required('catalog.change_bookinstance')
def change_bookinstance(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = ChangeBookinstanceForm(request.POST)

        #  Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            book_inst.borrower = form.cleaned_data.get('borrower')
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.status = form.cleaned_data['status']
            book_inst.save()

            request_url = request.build_absolute_uri()
            if re.match(r'.*/borrowed$', request_url):
                #  если отображение было вызвано из списка всех книг, взятых пользователями:
                return HttpResponseRedirect(reverse('all-borrowed') ) #  Переход по адресу 'all-borrowed':
            else:
                # иначе - отображение было вызвано из списка копий книги
                return HttpResponseRedirect(reverse('book-detail', args=[book_inst.book.pk]) ) #  Переход по адресу 'book-detail':

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        form = ChangeBookinstanceForm(initial=
                                      {'due_back': book_inst.due_back.__format__("%d-%m-%Y") if book_inst.due_back is not  None else None,
                                       'status': book_inst.status,
                                       "borrower": book_inst.borrower.username if book_inst.borrower is not None else None})

    return render(request, 'catalog/bookinstance_change.html', {'form': form, 'bookinst':book_inst})


class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_bookinstance'
    model = BookInstance
    success_url = reverse_lazy('genres')
    def get_success_url(self):
        book = self.object.book
        return reverse_lazy('book-detail', kwargs={'pk': book.id})
