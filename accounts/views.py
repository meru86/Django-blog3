from django.shortcuts import render, redirect
from allauth.account import views  # allauthaccountのviewsをimport
from django.views import View
from accounts.models import CustomUser
from accounts.forms import ProfileForm


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
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })



class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial = {
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'department': user_data.department,
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.department = form.cleaned_data['department']
            user_data.save()  # 入力データをデータベースに保存する
            return redirect('profile')  # 編集が完了したらプロフィール画面に遷移
        
        return render(request, 'accounts/profile.html', {
            'form': form
        })