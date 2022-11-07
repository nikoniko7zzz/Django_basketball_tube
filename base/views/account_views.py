from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # ログインしている人だけ
from django.contrib.auth import get_user_model
from base.models import Profile
from base.forms import UserCreationForm, ProfileCreateForm
from django.contrib import messages


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'pages/login_signup.html'

    def form_valid(self, form):
        messages.success(self.request, '新規登録が完了しました。続けてログインしてください。')
        return super().form_valid(form)

class Login(LoginView):
    template_name = 'pages/login_signup.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログインしました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'エラーでログインできません。')
        return super().form_invalid(form)

# ログインしている人だけが開けるページ
# login_requiredはdefのときに使うので
# 今回は、クラス用のLoginRequiredMixinを使う
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ('username', 'email', )
    success_url = '/account/' # 更新後も同じページを返す

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, 'アカウントを更新しました。')
        return super().post(request, *args, **kwargs)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    form_class = ProfileCreateForm
    # fields = ('name', 'tel', 'birth_day')
    success_url = '/profile/'

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, 'プロフィールを更新しました。')
        return super().post(request, *args, **kwargs)
