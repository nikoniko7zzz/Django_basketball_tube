# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from base.models import Item, Comment, Tag
from django.views.generic.edit import ModelFormMixin
from base.forms import CommentCreateForm, ItemCreateForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin # ログインしている人だけ



class IndexListView(LoginRequiredMixin, ListView):
    model = Item     # Itemモデルのデータを持ってくる
    template_name = 'pages/index.html'
    context_object_name = 'item_list'
    paginate_by = 8
    # paginate_by = 2 # テスト用

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tag_list'] = Tag.objects.all
        context['total_item'] = Item.objects.all().count()
        return context


class TagListView(IndexListView, ListView):
    paginate_by = 8
    # paginate_by = 2 # テスト用

    def get_queryset(self): # get_queryset の上書き
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(tag=self.tag)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['total_item'] = Item.objects.filter(tag=self.tag).count()
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        context['tag_name'] = self.tag
        return context



# Itemモデルのpkをもとに個別データを返す
# class ItemDetailView(DetailView):
#     model = Item
#     template_name = 'pages/item.html'


class ItemDetailView(ModelFormMixin, DetailView):
    """
    個別の動画ページ(item_detail.html)
    動画(Itemモデル)DetailViewとコメント投稿フォーム
    投稿->保存->リダイレクト
    """
    model = Item
    template_name = 'pages/item_detail.html'
    context_object_name = 'item'
    form_class = CommentCreateForm

    # no get_context_data override

    def post(self, request, *args, **kwargs):
        # first construct the form to avoid using it as instance
        form = self.get_form() # Formを取得
        self.object = self.get_object() # Itemのこと

        def form_valid(self, form):
            item = get_object_or_404(Item, pk=self.object.pk)
            comment = form.save(commit=False)
            comment.target = item
            comment.author = self.request.user
            comment.save()
            return HttpResponseRedirect(self.get_success_url())

        if form.is_valid():
            return form_valid(self, form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('item_detail', kwargs={'pk': self.object.pk})

    # 動画に紐づいたコメント数を返す
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        item = get_object_or_404(Item, pk=self.object.pk)
        self.target = item.pk
        context['comment_count'] = Comment.objects.filter(target=self.target).count()
        return context


# class ItemCreateView(LoginRequiredMixin, CreateView):
#     model = Item
#     form_class = ItemCreateForm
#     template_name = 'pages/item_create.html'
#     success_url = reverse_lazy('item_create')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['add_item_form'] = ItemCreateForm    #ここで定義した変数名
#         return context
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'pages/item_create.html'
    form_class = ItemCreateForm

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        item = form.save(commit=False)
        item.author = self.request.user
        item.save()
        return HttpResponseRedirect(reverse('item_create'))



# class CommentListView(ListView):
#     model = Comment
#     template_name = 'pages/comment.html'

class CommentListView(LoginRequiredMixin, ModelFormMixin, ListView):
    model = Comment
    template_name = 'pages/comment.html'
    # context_object_name = 'comment_objects'
    form_class = CommentCreateForm
    success_url = reverse_lazy('comment')

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form = self.get_form()

        def form_valid(self, form):
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.save()
            print('保存しました')
            return HttpResponseRedirect(reverse('comment'))

        if form.is_valid():
            return form_valid(self, form)
        else:
            return self.form_invalid(form)


class EveryoneCommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'pages/everyone_comment.html'

    # def get_success_url(self):
    #     return reverse_lazy('comment')

'''
class ItemDetailView(ModelFormMixin, DetailView)を作るにあたり参考にしたサイト

    - [参考url:詳細ビューとフォーム Mixin django の混合に関する問題](https://stackoverflow.com/questions/66503703/problem-with-mixing-detail-view-and-form-mixin-django)
    - [参考url:DjangoGithub](https://github.com/django/django/blob/3.0/django/views/generic/edit.py#L70)
    - [参考url:[Django] FormViewについて詳しく見てみる](https://e-tec-memo.herokuapp.com/article/285/)
    - [参考url:Djangoのクラスベースビューを完全に理解する](https://www.membersedge.co.jp/blog/completely-guide-for-django-class-based-views/)



if form.is_valid():
    return form_valid(self, form) # selfはつかないMy仕様で作成
else:
    return self.form_invalid(form)

***  解説  Djangoの動き(Dcuより)  ***
if form.is_valid():
    取得したFormのis_validを呼んで入力が正しいか検証して、
    正しければform_validメソッドを、
    何か不備があればform_invalidメソッドを呼ぶ

return form_valid(self, form)
    - 仕様の'self.form_valid(form)'の場合のDjangoの動き(Dcuより)

        # class FormMixinの時
        def form_valid(self, form)::
            """フォームが有効な場合、指定されたURLにリダイレクトします"""
            return HttpResponseRedirect(self.get_success_url())

        # class ModelFormMixin(FormMixin, SingleObjectMixin):の時
        def form_valid(self, form):
            """フォームが有効な場合、関連するモデルを保存する"""
            self.object = form.save()
            return super().form_valid(form)

        つまり、フォームが有効な場合、
        1. 関連するモデルを保存し
        2. 指定されたURLにリダイレクトします

    - 自作の 'form_valid(self, form)'を使う理由
        Commentモデルのauthorとtargetを一緒にsaveしたかったから

return self.form_invalid(form)
    def form_invalid(self, form):
        """フォームが無効な場合、無効なフォームをレンダリングする"""
        return self.render_to_response(self.get_context_data(form=form))
'''