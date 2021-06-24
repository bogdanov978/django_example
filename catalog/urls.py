from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
	path('', views.index, name='index'),
	
	url(r'^books/$', views.BookListView.as_view(), name='books'),
	url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
	
	url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
	url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),

	url(r'^genres/$', views.GenreListView.as_view(), name='genres'),

	url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	url(r'^books_borrowed/$', views.BorrowedBooksListView.as_view(), name='all-borrowed'),

	url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
	url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
	url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),

	url(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
	url(r'^book/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
	url(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),

	url(r'^genre/create/$', views.GenreCreate.as_view(), name='genre_create'),
	url(r'^genre/(?P<pk>\d+)/update/$', views.GenreUpdate.as_view(), name='genre_update'),
	url(r'^genre/(?P<pk>\d+)/delete/$', views.GenreDelete.as_view(), name='genre_delete'),

	url(r'^book/(?P<pk>\d+)/create_copy$', views.add_bookinstance, name='bookinstance_create'),
	url(r'^book/(?P<pk>[-\w]+)/update/$', views.change_bookinstance, name='bookinstance_update'),
	url(r'^book/(?P<pk>[-\w]+)/update/borrowed$', views.change_bookinstance, name='bookinstance_update_borrowed'),
	url(r'^book/(?P<pk>[-\w]+)/delete/$', views.BookInstanceDelete.as_view(), name='bookinstance_delete'),
]
