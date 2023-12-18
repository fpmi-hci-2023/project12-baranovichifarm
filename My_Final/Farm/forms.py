import pytz
import re
from datetime import datetime, timedelta

from django import forms

from Farm.models import User


class UserInfoForm(forms.Form):
    first_name = forms.CharField(
        label='First product',
        max_length=255,
        error_messages={'required': 'First product is required \u21b4'},
        widget=forms.TextInput(attrs={'size': 16}),
    )
    last_name = forms.CharField(
        label='Last product',
        max_length=255,
        error_messages={'required': 'Last product is required \u21b4'},
        widget=forms.TextInput(attrs={'size': 16}),
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Email is required \u21b4',
            'invalid': 'Enter a valid email address \u21b4', },
        widget=forms.TextInput(attrs={'size': 32}),
    )
    phone_number = forms.CharField(
        max_length=17,
        error_messages={'required': 'Phone number is required \u21b4'},
        widget=forms.TextInput(attrs={
            'placeholder': ' +375(29)111-11-11',
            'size': 13, }),
    )
    address = forms.CharField(
        max_length=255,
        error_messages={'required': 'Address is required \u21b4'},
        widget=forms.TextInput(attrs={'size': 30}),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pattern = '[+][3][7][5][(]\d\d[)]\d\d\d[-]\d\d[-]\d\d'
        match = re.fullmatch(pattern, phone_number)
        if not match:
            raise forms.ValidationError('Enter a valid phone number \u21b4')
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError('Enter a valid first product \u21b4')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError('Enter a valid last product \u21b4')
        return last_name

    def as_myp(self):
        return self._html_output(
            normal_row=f'<p style="margin-top: 5px; margin-bottom: 5px;">%(label)s %(field)s %(help_text)s</p>',
            error_row='<span style="color: red;">%s</span>',
            row_ender='',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        error_messages={'required': 'Login is required \u21b4'},
        widget=forms.TextInput(attrs={'size': 24}),
    )
    password = forms.CharField(
        max_length=255,
        error_messages={'required': 'Password is required \u21b4'},
        widget=forms.PasswordInput(attrs={'size': 24}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError('The user with that login was not found!')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if user and password and user.password != password:
            self.add_error('password', 'Incorrect password \u21b4')
        return cleaned_data

    def as_myps(self):
        return self._html_output(
            normal_row=f'<p>%(label)s %(field)s %(help_text)s </p>',
            error_row='<span style="color: red;">%s</span>',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)


class PreRegForm(SignInForm):
    conf_password = forms.CharField(
        label='Confirm password',
        max_length=255,
        error_messages={'required': 'Password confirmation is required \u21b4'},
        widget=forms.PasswordInput(attrs={'size': 22}),
    )


class RegForm(UserInfoForm, PreRegForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if not username.isalnum():
            raise forms.ValidationError('Enter a valid login \u21b4')
        if user:
            raise forms.ValidationError('The user with that login already exists \u21b4')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            raise forms.ValidationError('The user with that email already exists \u21b4')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        conf_password = cleaned_data.get('conf_password')
        if password and conf_password:
            if not password.isalnum() or len(password) < 10:
                self.add_error('password', 'Incorrect format for password \u21b4')
            if password != conf_password:
                self.add_error('conf_password', "Passwords don't match \u21b4")
        return cleaned_data


class CheckoutGuestForm(UserInfoForm):
    delivery_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M'],
        error_messages={
            'required': 'Delivery date is required \u21b4',
            'invalid': 'Enter a valid delivery date \u21b4', },
        widget=forms.TextInput(attrs={
            'placeholder': ' 20.02.2020 20:02',
            'size': 14, }),
    )
    comment = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={
            'cols': 40,
            'rows': 4, }),
        required=False,
    )

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data['delivery_date']
        utc = pytz.UTC
        min_delivery_date = utc.localize(datetime.now() + timedelta(hours=1))
        if delivery_date < min_delivery_date:
            raise forms.ValidationError('Enter a valid delivery date \u21b4')
        return delivery_date


class CheckoutUserForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        error_messages={'required': 'Address is required \u21b4'},
        widget=forms.TextInput(attrs={'size': 30}),
    )
    delivery_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M'],
        error_messages={
            'required': 'Delivery date is required \u21b4',
            'invalid': 'Enter a valid delivery date \u21b4', },
        widget=forms.TextInput(attrs={
            'placeholder': ' 20.02.2020 20:02',
            'size': 14, }),
    )
    comment = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={
            'cols': 40,
            'rows': 4, }),
        required=False,
    )

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data['delivery_date']
        utc = pytz.UTC
        min_delivery_date = utc.localize(datetime.now() + timedelta(hours=1))
        if delivery_date < min_delivery_date:
            raise forms.ValidationError('Enter a valid delivery date \u21b4')
        return delivery_date

    def as_myp(self):
        return self._html_output(
            normal_row=f'<p style="margin-top: 5px; margin-bottom: 5px;">%(label)s %(field)s %(help_text)s</p>',
            error_row='<span style="color: red;">%s</span>',
            row_ender='',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)
