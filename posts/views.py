from django.shortcuts import get_object_or_404, render

from django.db import models
from django.views.generic import ListView, TemplateView, DetailView, FormView, CreateView, UpdateView
from .models import *
from posts.forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify

class IndexView(ListView): # listelemek istedigimiz için list view
    template_name = 'posts/index.html'
    model = Post # burda diyorumki post modelimi listeliyecegim
    context_object_name = 'posts'
# context_object_name : Key
# posts : Value olarak düşün

    def context_object_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data(**kwargs)
        context['slider_posts'] = Post.objects.all().filter(slider_post=True)
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['slider_posts'] = Post.objects.all().filter(slider_post=True)
        # slider_post True olanları bana dönder
        return context



class PostDetail(DetailView):
    template_name = 'posts/detail.html'
    model = Post
    context_object_name = 'single'

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data(**kwargs)
        return context



class CategoryDetail(ListView):
    model = Post # postları listeledigimiz için
    template_name = 'categories/category_detail.html'
    context_object_name = 'posts'
    # burda bütün postları çek
    # kategoriye ait postları ayırmak içinde:
    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
# objem varsa dön yoksa hata sayfası gönder kwargs oluşturmamızın sebebi id sinide al
# o posta ait olanları nasıl dönderiyoruz:
        return Post.objects.filter(category=self.category).order_by('-id')
#category'si self.category olan order_by: en yeni olanı en önde getirsin
#parantez içindeki ilk category modelimizdeki category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetail,self).get_context_data(**kwargs)
        self.category = get_object_or_404(Category,pk=self.kwargs['pk'])
        context['category'] = self.category
        return context



class TagDetail(ListView):
    model = Post
    template_name = 'tags/tag_detail.html'
    context_object_name = 'posts'
 
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tag=self.tag).order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagDetail,self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag,slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context



@method_decorator(login_required(login_url='/users/login'),name='dispatch')
# burda post oluşturma sayfasına giriş yapan kullanıcı bu alana gelsin
class CreatePostView(CreateView):
    template_name = 'posts/create-post.html'
    form_class = PostCreationForm
    model = Post

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.pk, 'slug':self.object.slug})
# burda oluşturugumuz postun detay sayfasına git diyoruz

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        tags = self.request.POST.get('tag').split(',')
        # yazdıgımız tags bölye etiket dönmemizi saglıyor tags = ['etiket1','et2','et3']

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
# current_tag kullanmamızın sebebi, etiketlerimizin şöyle bir yapısı var 
# aldıgımız etiket daha önce database varsa database eklemicez! eğer yoksa ekliyecez
            
            if current_tag.count()<1:
# burda count: say demek eğer 1 den azsa yani yoksa diyoruz
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)

            else:
                exist_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(exist_tag)

        return super(CreatePostView,self).form_valid(form)



@method_decorator(login_required(login_url='/users/login'),name='dispatch')
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.pk, 'slug':self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user

        form.instance.tag.clear()

        tags = self.request.POST.get('tag').split(',')

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)

            else:
                exist_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(exist_tag)

        return super(UpdatePostView, self).form_valid(form)
        