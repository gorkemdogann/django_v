from django.db import models

from django.conf import settings
from django.template.defaultfilters import slugify
from PIL import Image

# önce kategory yukarıya yazmamız lazım.
class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(editable=False)
#editable=False yaptıgımızda otomatik kendisi atıyor slug alanını.

# admin panelimde gözükmesini istedigim şey title olsun diye str yaptık
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Category,self).save(*args,**kwargs)

# şimdi kategorilerimi saydırmak için fonk. yazıyorum:
    def post_count(self):
        return self.posts.all().count()
# return'deki posts geldiği yer: related_name='posts' Post sınıfının category modelinden.



class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="Etiket Adı")
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args,**kwargs)

    def post_count(self):
        return self.posts.all().count()
# tag modelinde aşşagıda related_name='posts' lullandıgımız için  
# post_count fonk. html'de çagırıyoruz



class Post(models.Model):
    title = models.CharField(max_length=150,verbose_name='Başlık')
    content = models.TextField(verbose_name='İçerik')
    date = models.DateField(auto_now_add=True,verbose_name='Zaman')
    image = models.ImageField(blank=True,null=True,upload_to='uploads/', default='uploads/215_resim.jpg', verbose_name="Fotoğraf")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1,verbose_name='Kullanıcı')
    slug = models.SlugField(default='slug', editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1,related_name='posts', verbose_name='Kategori')
    tag = models.ManyToManyField(Tag, related_name='posts', blank=True)
# ManyToManyField: bir tane tag bir sürü postu olabilir ve bir postata birden fazla tag olabilir
# ForeignKey ise: bir kategorinin bir çok postu olabilir. bir postun birden fazla katagorisi olamaz
    slider_post = models.BooleanField(default=False, verbose_name='Vitrin')
# Slider ana sayfadaki en üste fotografları saga çektigimiz yer.
# BooleanField: True or post mantıgı vardır, evetse göster.
# Default değere false verdik. adminden postlara girdigimizde vitrin diye bir şey çıktı onu görebiliyoruz

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args,**kwargs)

    def post_tag(self):
        return ','.join(str(tag) for tag in self.tag.all())