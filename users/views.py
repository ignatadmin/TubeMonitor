from linecache import cache
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, template_name="signup.html", context={"form": form})


def logout(request):
    django_logout(request)
    return redirect('index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        cache.clear()
        return reverse_lazy('index')
