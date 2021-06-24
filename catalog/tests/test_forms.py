from django.test import TestCase

import datetime
from catalog.forms import ChangeBookinstanceForm
from django.contrib.auth.models import User
from django.forms.forms import NON_FIELD_ERRORS


class ChangeBookinstanceFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user1',
                                 password='user1_password')

    def test_date_ok(self):
        date_ok = datetime.date.today() + datetime.timedelta(days=3)

        form_data = {'borrower': None, 'due_back': date_ok, 'status': 'm'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_date_in_past(self):
        date_in_past = datetime.date.today() - datetime.timedelta(days=3)
        form_data = {'borrower': None, 'due_back': date_in_past, 'status': 'm'}
        form = ChangeBookinstanceForm(data=form_data)

        self.assertTrue(form.has_error('due_back', code='date in past'))

    def test_status_a(self):
        # borrower is not None:
        user = User.objects.get(id=1)
        form_data = {'borrower': user.username, 'due_back': None, 'status': 'a'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='borrower is not none'))
        # date is not None:
        date_ok = datetime.date.today() + datetime.timedelta(days=3)
        form_data = {'borrower': None, 'due_back': date_ok, 'status': 'a'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='due_back is not none'))
        # valid form:
        form_data = {'borrower': None, 'due_back': None, 'status': 'a'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_status_o(self):
        # borrower is None:
        date_ok = datetime.date.today() + datetime.timedelta(days=3)
        form_data = {'borrower': None, 'due_back': date_ok, 'status': 'o'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='borrower is none'))
        # date is None:
        user = User.objects.get(id=1)
        form_data = {'borrower': user.username, 'due_back': None, 'status': 'o'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='due_back is none'))
        # valid form:
        form_data = {'borrower': user.username, 'due_back': date_ok, 'status': 'o'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_status_m(self):
        # borrower is not None:
        user = User.objects.get(id=1)
        form_data = {'borrower': user.username, 'due_back': None, 'status': 'm'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='borrower is not none'))
        # date is None:
        date_ok = datetime.date.today() + datetime.timedelta(days=3)
        form_data = {'borrower': None, 'due_back': None, 'status': 'm'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='due_back is none'))
        # valid form:
        form_data = {'borrower': None, 'due_back': date_ok, 'status': 'm'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_status_r(self):
        # полностью копирует test_status_m, за исключением статуса
        # borrower is not None:
        user = User.objects.get(id=1)
        form_data = {'borrower': user.username, 'due_back': None, 'status': 'r'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='borrower is not none'))
        # date is None:
        date_ok = datetime.date.today() + datetime.timedelta(days=3)
        form_data = {'borrower': None, 'due_back': None, 'status': 'r'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code='due_back is none'))
        # valid form:
        form_data = {'borrower': None, 'due_back': date_ok, 'status': 'r'}
        form = ChangeBookinstanceForm(data=form_data)
        self.assertTrue(form.is_valid())
