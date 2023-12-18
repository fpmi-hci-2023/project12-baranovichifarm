from My_Final.funcs import generate_logo
from Farm.models import User
from django.shortcuts import (render,
                              redirect, )
from Farm.forms import (SignInForm,
                        RegForm)
from verify_email.email_handler import send_verification_email

referer_list = []


def sign_in(request):
    signed_user = User.objects.filter(login=1).first()
    if request.method == 'GET':
        # определение урла, с которого была выполнена авторизация.
        referer = request.META.get('HTTP_REFERER')
        # если на страницу авторизации вход был через ввод ее урла в адресной строке,
        # то перенаправление будет на домашнюю страницу.
        if not referer:
            referer = '/'
        # проверка аутентификации пользователя.
        if signed_user:
            referer = referer_list[-1]
            # если на страницу авторизации вход был по ссылке, перенаправление будет на ту страницу,
            # где размещена ссылка
            if 'registration' not in referer:
                return redirect(referer)
            # если на страницу авторизации вход был по ссылке, перенаправление будет на ту страницу,
            # где размещена ссылка, игнорируя страницу регистрации пользователя.
            else:
                return redirect(referer_list[-2])
        else:
            referer_list.append(referer)
            form = SignInForm()
            return render(request, 'sign_in_page.html', {
                'logo_name': generate_logo(), 'form': form})
    elif request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = User.objects.filter(username=username)
            if password == user.first().password:
                user.update(login=1)
                return redirect('sign_in')
        return render(request, 'sign_in_page.html', {'logo_name': generate_logo(), 'form': form})


def registration(request):
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            del data['conf_password']
            data.update([('first_name', data.get('first_name').capitalize()),
                         ('last_name', data.get('last_name').capitalize())])
            User.objects.create(**data)
            return redirect('sign_in')
    return render(request, 'reg_page.html', {'logo_name': generate_logo(), 'form': form})
