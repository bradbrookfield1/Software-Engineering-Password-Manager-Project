from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import UserRegisterForm
from django.conf import settings
from cryptography.fernet import Fernet
from .models import Account

fernet = Fernet(settings.KEY)
allFields = ['name', 'username', 'email', 'password', 'link', 'notes']


class AccountListView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return Account.objects.filter(author=self.request.user)


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account


class BackToAccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Account

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.author:
            temp_password = account.password.encode()
            temp_password = fernet.encrypt(temp_password)
            account.password = temp_password.decode()
            account.save()
            return True
        return False


class AccountDetailViewShown(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Account
    template_name = 'passwordmanager/account_shown.html'

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.author:
            temp_password = account.password.encode()
            temp_password = fernet.decrypt(temp_password)
            account.password = temp_password.decode()
            account.save()
            return True
        return False


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = allFields

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            password = request.POST.get('password')
            encrypted_password = password.encode()
            encrypted_password = fernet.encrypt(encrypted_password)
            encrypted_password = encrypted_password.decode()
            Account.objects.create(
                name=request.POST.get('name'),
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=encrypted_password,
                link=request.POST.get('link'),
                notes=request.POST.get('notes'),
                author=request.user,
            )
            messages.success(request, f'Account created successfully!')
            return redirect('account-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    fields = allFields

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            password = request.POST.get('password')
            encrypted_password = password.encode()
            encrypted_password = fernet.encrypt(encrypted_password)
            encrypted_password = encrypted_password.decode()
            account = self.get_object()
            account.name = request.POST.get('name')
            account.username = request.POST.get('username')
            account.email = request.POST.get('email')
            account.password = encrypted_password
            account.link = request.POST.get('link')
            account.notes = request.POST.get('notes')
            account.author = request.user
            account.save()
            messages.success(request, f'Account updated successfully!')
            return redirect('account-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.author:
            return True
        return False


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    success_url = '/'

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.author:
            return True
        return False


@login_required
def profile(request):
    return render(request, 'passwordmanager/profile.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account made for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'passwordmanager/register.html', {'form': form})
