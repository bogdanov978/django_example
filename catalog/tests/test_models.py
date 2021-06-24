from unittest import TestCase

from django.test import TestCase
import re
from catalog.models import Genre, Author, Book, BookInstance


class CatalogModelBaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

        Genre.objects.create(name='Science fiction')
        Genre.objects.create(name='Cooking')
        Genre.objects.create(name='Health')
        Genre.objects.create(name='Travel')

        Book.objects.create(title="book1", author=Author.objects.get(id=1), summary="summary1", isbn="0000000000001")
        Book.objects.get(id=1).genre.set(Genre.objects.all())

        BookInstance.objects.create(book=Book.objects.get(id=1), imprint="imprint1", status='o', due_back="2022-01-01") #  is_over_due-->false
        BookInstance.objects.create(book=Book.objects.get(id=1), imprint="imprint1", status='o', due_back="2021-01-01") #  is_over_due-->true
        BookInstance.objects.create(book=Book.objects.get(id=1), imprint="imprint1", status='a')  #  is_over_due-->false (due_back is None)

class GenreModelTest(CatalogModelBaseTest):
    def test_str(self):
        genre = Genre.objects.get(id=1)
        self.assertEquals(str(genre), 'Science fiction')


class BookModelTest(CatalogModelBaseTest):
    def test_str(self):
        book = Book.objects.get(id=1)
        self.assertEquals(str(book), 'book1')

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.get_absolute_url(), '/catalog/book/1')

    def test_display_genre(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.display_genre(), 'Cooking, Health, Science fiction')


class BookInstanceModelTest(CatalogModelBaseTest):

    def test_str(self):
        book_inst = BookInstance.objects.filter(book__title__exact = "book1")[0]
        regex = r'.*\(' + str(book_inst.book.title) + '\)$'
        self.assertIsNotNone(re.match(regex, str(book_inst)))

    def test_is_overdue(self):
        book_inst = BookInstance.objects.filter(book__title__exact="book1")[0]
        self.assertIs(book_inst.is_overdue, False)

        book_inst = BookInstance.objects.filter(book__title__exact="book1")[1]
        self.assertIs(book_inst.is_overdue, True)

        book_inst = BookInstance.objects.filter(book__title__exact="book1")[2]
        self.assertIs(book_inst.is_overdue, False)


class AuthorModelTest(CatalogModelBaseTest):

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')
