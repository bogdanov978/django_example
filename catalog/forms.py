from django import forms

from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
import datetime
from .models import BookInstance
from django.contrib.auth.models import User


class AddBookinstanceForm(forms.Form):
    imprint = forms.CharField()


class ChangeBookinstanceForm(forms.Form):
    USER_CHOICES = [(u.username, u.username) for u in User.objects.all()] + [(None, "")]
    borrower = forms.ChoiceField(choices=USER_CHOICES, required=False)

    due_back = forms.DateField(required=False, input_formats=('%d-%m-%Y', '%Y-%m-%d'), label="Due to be returned")

    status = forms.ChoiceField(choices=BookInstance.LOAN_STATUS)

    def clean_borrower(self):
        data = self.cleaned_data['borrower']
        data = User.objects.filter(username__exact=data).get() if data != "" else None
        return data

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data is None:
            return None

        if data < datetime.date.today():
            raise ValidationError('Invalid date - renewal in past', code = 'date in past')

        return data

    def clean(self):
        status = self.cleaned_data.get('status')
        borrower = self.cleaned_data.get('borrower')
        due_back = self.cleaned_data.get('due_back')
        if status == 'a':
            #  если книга доступна, у нее не должно быть взявшего ее пользователя и даты возвращения
            if borrower is not None:
                raise ValidationError('If status is "Available", Borrower field must be empty', code = 'borrower is not none')

            if due_back is not None:
                raise ValidationError('If status is "Available", Due back field must be empty', code = 'due_back is not none')
        elif status == 'o':
            #  если книга взята пользователем, должно быть указано имя пользователя и дата возвращения
            if borrower is None:
                raise ValidationError('If status is "On loan", Borrower field must not be empty', code = 'borrower is none')

            if due_back is None:
                raise ValidationError('If status is "On loan", Due back field must be set', code = 'due_back is none')
        else:
            #  если книга на обслуживании или зарезервирована, имя пользователя должно быть пустым, но дата возвращения должна быть указана
            if borrower is not None:
                raise ValidationError('If status is "Maintenance" or "Reserved", Borrower field must be empty', code = 'borrower is not none')

            if due_back is None:
                raise ValidationError('If status is "Maintenance" or "Reserved", Due back field must be set', code = 'due_back is none')
