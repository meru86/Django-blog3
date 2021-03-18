from django.shortcuts import render, redirect
from allauth.account import views  # allauthaccountのviewsをimport
from django.views import View


# LoginViewクラスを作成します。引数にallauthのLoginViewを継承させます。
class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')  # トップページにredirect

class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/profile.html')