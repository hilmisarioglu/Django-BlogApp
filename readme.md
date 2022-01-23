# Virtual enviroment olusturuyoruz. Sonra activate ediyoruz 
py -m venv benv 
source ./env/Scripts/activate
# Django yüklüyoruz.  
pip install django
# Sonrasinda decouple ve pillow yüklenir. Djangoda img kullanmak icin pillow kütüphanesi yüklenir.
pip install python-decouple
pip install pillow
# Eger kullanilacaksa crispy forms yüklenir. 
pip install django-crispy-forms
# Requirements dosyasi olusturalim. 
pip freeze > requirements.txt
# .gitignore dosyasi koyalim. 
# Projeyi olusturalim 
django-admin startproject cblog
# App olusturalim 
py manage.py startapp blog
# Installed app e yazalim.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my_apps
    # 'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'blog',
    #third_party
    'crispy_forms',
]
# Decouple ayarlarini yapalim ve SECRET_KEY olusturalim
from decouple import config
SECRET_KEY = config('SECRET_KEY')
# .env dosyasi olustur SECRET_KEY yapistir.
SECRET_KEY = D)DZ§"()ZD()HEDKLSNJAS%&%&78678678s
# Application ayarlarini yaptik.Settingste django decouple paketini kullaniyoruz. Ana klasör altinda .env klasörü olusturulur. Product a olmasini istemedigimiz seyleri env dosyasinin icine yaziyoruz.Bu dosya bazi dosyalarin gizli kalmasini sagliyor. Projenin sonunda database i postgresql e baglicaz. Buradaki kullanici adi ve sifrelerini de env dosyasina koyacagiz. 
# Application lari admin panelde görebilmek icin migrate komutunu uyguluyoruz.
py manage.py migrate  
# Sonra superuser olusturuyoruz
py manage.py createsuperuser
# Projeyi calistirip admin panele bak 
py manage.py runserver 
------------------------------------------------------------------
# urls.py ayarlarini yapacagiz. Bos geldiginde bizi blog.urls e yönlendirecek. 
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
----------------------------------------------------------------
# Simdi nasil modellerimiz olacak yazalim. Category ve Post modellerimiz olacak. Bunlarin icinde bazi fields ler olacak. Comment ve like tablolarimiz olacak.


# Djangonun boze otomatik verdigi bir user modeli var. Öncelikle ondan bahsedelim. 
Django Default User Model Fields
Here is the list of default Django user fields.

#	User Model Field	Data Type	Description
# 1	_state	ModelState	It is used to preserve the state of the user.
# 2	id	Number	Unique ID for each user.
# 3	password	string	Encrypted password for the user.
# 4	last_login	datetime	Date and time when user logged in last time.
# 5	is_superuser	bool	True if the user is superuser, otherwise false.
# 6	username	string	Unique username for the user.
# 7	first_name	string	First name of the user.
# 8	last_name	string	Last name of the user.
# 9	email	email	Email ID of the user.
# 10	is_staff	bool	Set true if the user is a staff member, else false.
# 11	is_active	bool	Is profile active.
# 12	date_joined	datetime	Date and time when the user joined the first time. It is usually when the user signs up or creates a user account the first time

from django.db import models

# Yukarida bahsedilen user modeli auth da sakli.
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'blog/{0}/{1}'.format(instance.author.id, filename)

# Category modeli parent modelim olacak post ise child. Bu model dropdown menü olacak ve sadece admin panelinden giris yapilabilecek. Cünkü her önüne gelen user category olustursun istemiyoruz. 
class Category(models.Model):
    name = models.CharField(max_length=100)
    
# Categorys yerine DB de Categories gözükecek
    class Meta:
        verbose_name_plural = "Categories"
        
# db de nasil gözüksün onu gösterir
    def __str__(self):
        return self.name

class Post(models.Model):
    OPTIONS = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
  
    title = models.CharField(max_length=100)    

    content = models.TextField()

    image = models.ImageField(upload_to=user_directory_path, 
    default='django.jpg')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)

# Olusturuldugunda otomatik olarak tarih verecek
    publish_date = models.DateTimeField(auto_now_add=True) 
# Otomatik olarak djangonun model fields lerin özelliginden dolayi bir parametre oluyor, her update edildiginde güncel tarihi aliyor. 
    # last_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

# draft-published field i olacak. Eger yazar blogun ana sayfada yayinlanmasini istemiyorsa drafti sececek. 
    status = models.CharField(max_length=10, choices=OPTIONS, default='d')

# Bir "slug", genellikle önceden elde edilmiş verileri kullanarak geçerli bir URL oluşturmanın bir yoludur. Örneğin, bir bilgi, bir URL oluşturmak için bir makalenin başlığını kullanır. Slug'u manuel olarak ayarlamak yerine, başlık (veya başka bir veri parçası) verilen bir işlev aracılığıyla oluşturmanızı tavsiye ederim.Aralara - koyarak URL olusturur. slug how-to-learn-django-7636fgseze2 gibi
    slug = models.SlugField(blank=True)
# ----------------------------------------------------------------
# admin.py yazalim.
from django.contrib import admin
from .models import  Post, Category

admin.site.register(Category)
admin.site.register(Post)
# ----------------------------------------------------------------
# fotolari media_root isminde bir directiry ac ve altina kaydet demek.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media_root"

# ana projedeki urls.pyy a git ve bir kac ayar var onlari yap.
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('users/', include('users.urls')),
]

# gelistirme asamasindayken media file larimi benim gösterdigim klasör altina koy, production asamasina geldigimizde ben baska bir yol verecem demek. media_root isminde bir klasör olustur.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# modelde bir fonksiyon belirle, upload_to ile de bu fonksiyonu cagir. media_root un altina blog isminde klasör acacak, onun da altina yazarin id numarasinin oldugu bir klasör acacak , onun da altina dosya isimlerini yazacak.Otomatik olarak kendi olusturacak.
def user_directory_path(instance, filename):
    return 'blog/{0}/{1}'.format(instance.author.id, filename)

image = models.ImageField(upload_to=user_directory_path, default='django.jpg')  
# ----------------------------------------------------------------
# signals.py dan bahsedelim. Bir post olusturulmadan önce prepost veya olusturuldak sonra postsave , postdelete vs ne yapmak istiyorsak bunlari signals dosyasi altina yazariz. 

# apps.py 
    def ready(self):
        import blog.signals

# signals.py
# post etmeden önce bana slug olustur demek pre_save methodu
from django.db.models.signals import pre_save 
# kaydete bastiktan sonra önce ben bi islem yapacam onu yaptiktan sonra kaydet demek yani dispatcherin recevir fonksiyonu. Mesela herhangi bir blog u sildikten sonra ona ait fotolari da sil.
from django.dispatch import receiver
# araya tire koyan bir fonksiyon var slugify, methodun icerisine koydugum stringleri arasina bosluk koyuyor yaptigi islem bu aslinda.
from django.template.defaultfilters import slugify
from .models import Post
# sonuna rastgele 8 basamakli ifade koyar
from .utils import get_random_code

@receiver(pre_save, sender=Post)
def pre_save_create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + ' ' + instance.title)
a = 'hilmi sarioglu'
print(slugify(a))
# hilmi-sarioglu ciktisini verir
# ----------------------------------------------------------------

# models.py a PostView , Comment ve Like  adinda class yaziyoruz ve admin panele geciriyoruz
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Post u kac kisi görüntülemis bunu tutmak icin
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
# --------------------------------------------------------------
from django.contrib import admin
from .models import  Post, Comment, Like, PostView, Category

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(Like)
# --------------------------------------------------------------
# forms.py olusturuyoruz. Benim 2 tane forma ihtiyacim var. PostForm ve CommentForm. PostFormu edit islemleri yaparken de kullanacagiz. Digerini de yorum icin olusturacagiz. 
from django import forms
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
# Postun icindeki options lari dogrudan burada da kullanabiliriz. Dropdown yapar
    status = forms.ChoiceField(choices=Post.OPTIONS)
# Category tableinda db de eklendikce buraya da dropdown olarak eklenir.ModelChoiceField araciligi ile, Bos iken ise Select yazacak.
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select" )
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'image',
            'category',
            'status',
        )
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
# ----------------------------------------------------------------
# Simdi views yazmaya baslayalim. Her view yazildiktan sonra template yazilir ve entegreli bir sekilde devam edilir.

from django.shortcuts import render

def post_list(request):
    qs = Post.objects.filter(status='p')
    context = {
        'object_list' : qs
    }
    return render (request, "blog/post_list.html", context )
# Bu benim base templates im olacak. Bunun icerisine diger templatesler koyulacak. BaseTemplates icin settings e gidilir.
TEMPLATES = [
    {
        'DIRS': [BASE_DIR, "templates"],
]
# Daha sonra templates klasörü altinda base.html olusturulur.

<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>

# -------------------------------------------------------------  
# templates/blog/post_list.html
{% extends 'base.html' %}

{% block content %}
{% for object in object_list %}
<h1>{{object.title}}</h1>
<img src="{{object.image.url}}" alt="">

# 20 karakter göstersin sonuna da 3 nokta koyar
<p>{{object.content | truncatechars:20}}</p>
{{ endfor }}
{% endblock content %}


# simdi url ye isleyelim
from django.urls import path
from .views import post_list

app_name = "blog" 
urlpatterns = [
    path("",post_list, name="list"),
]
# -------------------------------------------------------------
# views yazmaya devam edelim
from .forms import PostForm
def post_create(request):
    # form = PostForm(request.POST or None, request.FILES or None)
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # print(request.FILES)
        if form.is_valid():

# author u database e söylemem lazim bunu kim yaziyor diye. commit = False demek datayi sen kaydet ama daha database e isleme, ben bir sey ekleyecegim bu post a demek. 
            post = form.save(commit=False)
# burda da author u user a esitledik. Burada author u doldurduk. Yani kullaniciya author bölümün doldurtmadik onun yerine yolda bunu ben ekledim. Bu cok kullanilan bir yapi. Eger bu bölümü es gecersek bize hata verir. Post has no author hatasi aliriz.
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
# app_name diye bir sey yazdik, djangonun kafas karismasin diye, list e redirect yapacak ama hangi list e ? Blog altindaki list.
            return redirect("blog:list")
    context = {
        'form' : form
    }
    return render (request, "blog/post_create.html", context)

# hemen urls e ekliyoruz
from django.urls import path
from .views import post_list, post_create

app_name = "blog" 
urlpatterns = [
    path("",post_list, name="list"),
    path("create/",post_create, name="create"),
]

# templates/blog/post_create.html olusturalim. 
{% extends 'base.html' %} {% load crispy_forms_tags %} {% block content %}
<div class="row">
  <div class="col-md-6 offset-md-3">
    <h3>Blog Post</h3>
    <hr />

# multipart/form-data yazmazsak bize hep default resimleri yükler, bizim yükledigimiz fotograflari sergilemez.
    <form method="POST" enctype="multipart/form-data">   
      {% csrf_token %} {{form|crispy}}
      <br />
      <button type="submit" class="btn btn-outline-info">Post</button>
    </form>
  </div>
</div>

{% endblock content %}
# -------------------------------------------------------------
# utils.py yaziyoruz
# uuid bana random harlerden ve rakamlardan bir string üretir
import uuid

def get_random_code():
    code = str(uuid.uuid4())[:11].replace("-","")
    return code

# signals.py i güncelleyebiliriz
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Post
from .utils import get_random_code

@receiver(pre_save, sender=Post)
def pre_save_create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + " " + get_random_code())

# -------------------------------------------------------------
# views yazmaya devam edelim
# eskiden id tanimliyordum simdi slug field gelecek 
def post_detail(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    context = {
        'object' : obj,
    }
    return render(request, "blog/post_detail.html", context)

# templates/blog/post_detail.html olusturalim. Burda da CommentForm u gösterecegiz.post_list e benzer olacak.
{% extends 'base.html' %}
{% block content %}
<h1>{{object.title}}</h1>
<img src="{{ object.image.url }}" alt="">
<p>{{object.content}}</p>
{% endblock content %}

# urls.py a gidip details i ekle
urlpatterns = [
    path("",post_list, name="list"),
    path("create/",post_create, name="create"),
    path("<str:slug>/",post_detail, name="detail"),
]

#  Ben post_list teki title a tikladigimda beni ilgili post_details e yönlendirecek. Bunun icin sunlar yapilir.Öncelikle post_list i güncelle. a tag ini ekle. Title i da a taginin icine koy

{% extends 'base.html' %}
{% block content %}
{% for object in object_list %}
<a href="{% url 'blog:detail' object.slug %}"><h1>{{object.title}}</h1></a>
<img src="{{object.image.url}}" alt="">
# 20 karakter göstersin sonuna da 3 nokta koyar
<p>{{object.content | truncatechars:20}}</p>
{{ endfor }}
{% endblock content %}

# -------------------------------------------------------------
# views i yazmaya devam. update icin bana request gerekiyor. slug gerekiyor. Burda ben yine bir obje alacagim. slug = slug diyecegim. form, objenin icerisi post ise request.POST olacak, yoksa none olacak, yani formun ici bos olacak. Ve ben update ederken file i da aliyorum. Ve bana gelirken icerisinin dolu olmasi icin instance alacagim. instance benim sectigim objeye esit olacak. update sayfasinda ne göstereceksem context e atip gönderiyorum. Yani object ve formu

def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)

    if form.is_valid():
        form.save()
        messages.success(request, "Post updated !!")
        return redirect("blog:list")
    context = {
        "object" : obj,
        "form" : form
    }
    return render(request, "blog/post_update.html", context)

# templates/blog/post_update.html olusturalim.
{% extends 'base.html' %} 
{% block content %}
    <h3>Update {{object.title}}</h3>
    <form method="POST" enctype="multipart/form-data">
      {% csrf_token %} 
      {{form.as_p}}
      <button type="submit">Update</button>
    </form>
{% endblock content %}

# urls.py a gidip update i ekle, yukarida da import etmeyi unutma.
urlpatterns = [
    path("",post_list, name="list"),
    path("create/",post_create, name="create"),
    path("<str:slug>/",post_detail, name="detail"),
    path("<str:slug>/update/",post_update, name="update"),
]

# -------------------------------------------------------------
# views i yazmaya devam. delete.
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Post deleted !!")
        return redirect("blog:list")
    context = {
        "object" : obj
    }
    return render(request, "blog/post_delete.html", context)

# urls.py a gidip delete i ekle, yukarida da import etmeyi unutma.
urlpatterns = [
    path("",post_list, name="list"),
    path("create/",post_create, name="create"),
    path("<str:slug>/",post_detail, name="detail"),
    path("<str:slug>/update/",post_update, name="update"),
    path("<str:slug>/delete/",post_delete, name="delete"),
]
# templates/blog/post_delete.html olusturalim. Kullanici cancel a basarsa onu baska bir yere (list e) redirect edecegiz Yes e basarsa silecegiz. 
{% extends 'base.html' %}
{% block content %}
<p>Are you sure you want to delete "{{object}}"?</p>
<form action=" " method="POST">
    {% csrf_token %}
    <a href="{% url 'blog:list' %}">Cancel</a>
    <button type="submit">Yes</button>
</form>
{% endblock %}

# -------------------------------------------------------------
# bootstrap ile html sayfalarini güzellestirelim. 
# base.html düzenle
{% load static %}
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <link rel="stylesheet" href="{% static 'blog/main.css' %}">
    <title>Blog Project</title>
  </head>
  <body>
      {% include 'navbar.html' %}
      <div class="container">
        {% if messages %}
        {% for message in messages %}

        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>

        {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
    <script src="https://kit.fontawesome.com/74c8282b8a.js" crossorigin="anonymous"></script>
  
  </body>
</html>

# -------------------------------------------------------------
# bootstrap ile html sayfalarini güzellestirelim. 
# navbar ekle. templates altina navbar.html ekle  
<header class="site-header">
    <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
        <div class="container">

# Clarusway Blog a tikladigimda beni list e yönlendirsin.homepage yani
            <a class="navbar-brand mr-4" href="{% url 'blog:list' %}">Clarusway Blog</a>
            
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle"
                aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarToggle">
                <div class="navbar-nav mr-auto">
                    <a class="nav-item nav-link" href="{% url 'blog:list' %}">Home</a>
                    <a class="nav-item nav-link" href="#">About</a>
                </div>
                <!-- Navbar Right Side -->
                <div class="navbar-nav">
                    {% if user.is_authenticated %}
                    <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
                    <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
                    <a class="nav-item nav-link" href="{% url 'blog:create' %}">New Post</a>
                    {% else %}
                    <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
                    <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>
</header>

# -------------------------------------------------------------

# blog/static/blog/main.css dosyasi olustur. Django eger html dosyasi icine css yazmayacaksak, baska bir dosya olarak import edeceksek bize bir sart kosuyor. static file. Sonra base.html ye alttaki linki ekle. settings te söyle bir sey de yazmis olabilirdik. STATICFILES_DIRS = BASE_DIR / 'static' o zaman static folderinin altina blog folder i acmaya gerek kalmazdi. Aslinda 2 cesit static files var.Birincisi basedir altinda digeri ise app in altinda eger basedir altinda staticfile yazmak istersek yukaridaki komut yazilir, app icine yazmak istersek projedeki gibi kalir. Basina BASE_DIR yazilmaz.
<link rel="stylesheet" href="{% static 'blog/main.css' %}">

# base.html dosyasinin en üstüne ise sunu ekle
{% load static %}

# navbar da base html ye ekli oldugu icin navbara da css kodu yazilabilir. 

body {
    background-color: #fafafa;
    color: #333333;
    margin-top: 5rem;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #444444;
}

ul {
    margin: 0;
}

.bg-steel {
    background-color: #d0f01b;
}

.site-header .navbar-nav .nav-link {
    color: #cbd5db;
}
.site-header .navbar-nav .nav-hover {
    color: #ffffff;
}
.site-header .navbar-nav .nav-link.active {
    font-weight: 500;
}

.content-section {
    background-color: #ffffff;
    padding: 10px 20px;
    border: 1px solid #ddd;
    border-radius: 3px;
    margin-bottom: 20px;
}

.account-img {
    height: 110px;
    width: 110px;
    margin-right: 20px;
    margin-bottom: 16px;
}

.account-heading {
    font-size: 2.5rem;
}

# -------------------------------------------------------------
# bootstrap ile post_list.html düzenle 
# base.html ye sunu yapistir
icon linki : https://fontawesome.com/v5.15/icons/comments?style=solid
<script src="https://kit.fontawesome.com/74c8282b8a.js" crossorigin="anonymous"></script>

# sonra post_list e gel
{% extends 'base.html' %}


{% block content %}
<h1 style="text-align: center;">Clarusway Blog</h1>
<div class="row mt-5" >
    {% for obj in object_list %}
    <div class="col-4">

        <div class="card shadow p-3 mb-5 bg-white rounded" style="width: 18rem; height: 25rem; ">
            <img src="{{ obj.image.url }}" class="card-img-top" alt="post_image" style="width:15rem; height: 11rem; align-self:center;">
            <hr>
            <div class="card-body">
                <h5 class="card-title"><a href="{% url 'blog:detail' obj.slug %}">{{obj.title}}</a></h5>
                <p class="card-text">{{obj.content|truncatechars:20}}</p>
                
                <p>
                    <span><i class="far fa-comment-alt ml-2"></i>{{ obj.comment_count }}</span>
                    <span><i class="fas fa-eye ml-2"></i>{{ obj.view_count }}</span>
                    <span><i class="far fa-heart ml-2"></i>{{ obj.like_count }}</span>
                <p class="card-text"><small>

# su kadar saat önce post edildi demek icin timesince 
                        Posted {{ obj.publish_date|timesince }} ago.
                    </small>
                </p>

                </p>
            </div>
        </div>
    </div>

    {% endfor %}
</div>
{% endblock content %}

# -------------------------------------------------------------
# LIKE , COMMENT , VIEW sayisini gösterme
# models e gidip yazmaya devam ediyoruz

# modelde tanimladigimiz Count , Like , PostView vs bunlar child. Biz ama parent olan posttaki toplam sayilari almamiz gerekiyor. Bu sebeple bir fonksiyon yaziyoruz. öncelikle modelde tanimlanan ismin kücük farfle yazimi sinra alt cisgi sonra da set yaziyoruz. Ör;  comment_set.all().count() böylelikle ilgili posta ait kactane comment varsa onlari verir.
def comment_count(self):
        return self.comment_set.all().count()
    
    def view_count(self):
        return self.postview_set.all().count()
    
    def like_count(self):
        return self.like_set.all().count()
    
    def comments(self):
        return self.comment_set.all()

# post_detail.html sayfasini yazalim . forms ta CommentForm olusturmustuk. Kullanici girisi oldugu yerde firm kullanilir. Comment yazarken de form yapisi kullanilacak bu sebepten ötürü commentform yazdik. Bu formu alip views e import edip post_view altinda alacam ve template e gönderecegim. 
def post_detail(request, slug):
    # comment = Comment.objects.all( )
    # kim = request.user
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug)
    # like_qs = Like.objects.filter(user=request.user, post=obj)
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=obj)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:

# formu database e kaydetmeden önce icini user ve post ile doldurmam gerekiyor. bunun icin öncelikle commit = False yaptik, db ye kaydetmemesi icin sonrada takibeden satirlari yazdik.  
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = obj
            comment.save()
            return redirect("blog:detail", slug=slug)
            # return redirect(request.path)
    context = {
        'object' : obj,
        "form" : form,
        # "like_qs" : like_qs,
        # 'kitap' : comment,
        # 'kim': kim
    }
    return render(request, "blog/post_detail.html", context)

# post_detail.html  
# like butonu koyacagim , her like ettiginde like sayisini 1 artirsin. Bunu yaparken öncelikle views e gidip like methodu yaziyoruz.
def like(request, slug):
    if request.method == "POST":
        obj = get_object_or_404(Post, slug=slug)
# database de benim yaptigim like var mi? user i suanki user a postu da suanki post a esitledik ve filtreledik.
        like_qs = Like.objects.filter(user=request.user, post=obj)
# exist methodunu kullaniyorum. bana queryset dönüyor, icerisindeki elemana ulasmak icin [0] yaptik, eger true ise bunu siliyorum delete() 
        if like_qs.exists():
            like_qs[0].delete()
# yoksa da yeni bir like create edecek
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect("blog:detail", slug=slug)
    return redirect("blog:detail", slug=slug)
# Like butonuna tekrar basarsam silinsin istiyorum. Bir de sunu kontrol edecegim, bu postun like i benim tarafimdan verilmis mi verilmemis mi? Eger daha önce verilmisse like i bir azaltack ilk defa verilmisse 1 artiracak. Yani bir kullanici sadece bir defa like verebilecek. 10 defa veremeyecek. Bu arada lie butonuna bastigimizda tüm sayfayi yenilemesin istiyorsak ajax komutu kullanilabilir.

# urls.py da like icin url belirleyelim
    path("<str:slug>/like/",like, name="like"),

# simdi post_detail.html ye gidebiliriz.

{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}

    <div class="container card" style="width: 40rem;">
        <img src="{{ object.image.url }}" class="card-img-top" alt="post_image">
        <div class="card-body">
            <h2 class="card-title">{{ object.title }}</h2>
            <hr>

            <div>
                <span><i class="far fa-comment-alt ml-2"></i></i> {{ object.comment_count }}</span>
                <span><i class="fas fa-eye ml-2"></i> {{ object.view_count }}</span>
                <span><i class="far fa-heart ml-2"></i> {{ object.like_count }}</span>
                <span class="float-right"> <small>Posted {{ object.publish_date|timesince }} ago.</small> </span>
            </div>
            <hr>

            <p class="card-text">{{ object.content }}.</p>
            <hr>

            <div>
            <h4>Enjoy this post? Give it a LIKE!!</h4>
            </div>

            <div>

# aslinda alt tarafta sunu yapti. Button submit edildiginde form action i calistirdi, diger inputlari hidden yaptigi icin onlar gözükmedi, bu sayede butona tikladiginda like_count u güncellemis oldu.
            <form action="{% url 'blog:like' object.slug %}" method="POST">
                {% csrf_token %}
                <input type="hidden" name="post">
                <input type="hidden" name="user">

# icon seklinde buton yapiyoruz.
                <button type="submit"><i class="fas fa-heart"></i></button>
                {{object.like_count }}
            </form>

            <hr>
            <!-- {% if user.is_authenticated %} -->
            <h4>Leave a comment below</h4>
            <form action="" method="POST">
                {% csrf_token %}
                {{form|crispy}}
                <button class="btn btn-secondary btn-sm mt-1 mb-1">SEND</button>
            </form>
#     def comments(self):
#        return self.comment_set.all()
# models e yukaridaki methodu yazmistik. Bu method ile tüm yorumlara ulasabilirim. Daha sonra post_detail e gidiyoruz ve for ile tüm commentsleri dönüyoruz. iki hr tagi arasindaki kisim alt alta tüm commentleri sergiler.
            <hr>
            <h4>Comments</h4>
            {% for comment in object.comments %}
            <div>
                <p>

# comment in kac saat önce yapildigi yaziyor.
                    <small><b>Comment by {{comment.user}}</b></small> - <small>{{ comment.time_stamp|timesince }} ago.
                    </small>
                </p>
                <p>
                    {{ comment.content }}

                </p>
            </div>
            <hr>
#     
 
            {% endfor %}
            <!-- {% else %} -->
            <!-- <a href="#" class="btn btn-primary btn-block">Login to comment</a> -->
            <!-- {% endif %} -->
        
        </div>

        </div>

        <div class="m-3">

# her authenticate olan edit update yapamamasi layim , herhangi blogu update delete yapabilmek icin user in ayni yamanda author olmasi gerekir. Bunun icin asagidaki kodu yazdik. 
        {% if user.id == object.author.id %}
        <a href="{% url 'blog:update' object.slug %}" class="btn btn-info">Edit</a>
        <a href="{% url 'blog:delete' object.slug %}" class="btn btn-danger">Delete</a>
        {% endif %}
    </div>
    <!-- <div>
        
        {% for i in kitap  %}
        
        {% if i.user == user %}
        <h1>{{i.content}}</h1>       
        {% endif %}
               
        {% endfor %}
     
    </div> -->
    <!-- <div>
        <h3>{{like_qs}}</h3>
    </div> -->

{% endblock content %}


# 
# ------------------------------------------------------------- 
# her authenticate olan edit update yapamamasi lazim , herhangi blogu update delete yapabilmek icin user in ayni yamanda author olmasi gerekir demistik. Bunun icin yukaridaki kodu yazdik. Fakat bu da yetmez, su an url güvenli degil. Adam url nin sonuna update veya delete yazarak da baskasinin postuna müdahele edebilir. Bunu da engellemek gerekiyor. Bunu biz view de koruyabiliriz. 
@login_required()
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)

# user ile author esit mi sorgusu
    if request.user.id != obj.author.id:
        # return HttpResponse("You are not authorized!")
        messages.warning(request, "You are not a writer of this post !")
        return redirect("blog:list")
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Post deleted !!")
        return redirect("blog:list")
    
    context = {
        "object" : obj
    }
    return render(request, "blog/post_delete.html", context)
    
# -------------------------------------------------------------
# crispy-forms yüklemeye geldi sira. Crispy-forms default olarak uni_form ile geliyor, biz bootstrap 4 e cevirecegiz. Form u bootstrape göre düzenliyor. Belki bootstrap5 e cevrilebilir.

# py -m pip install django-crispy-forms ile yükle
INSTALLED_APPS = [
 #third_party
    'crispy_forms',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Installed apps e ekledikten sonra bootstrap4 ayari yapilir.post_create i güncelleyecegiz.Asagidaki gibi.Formun fieldini kücültmek icin div icine al sonra onu kücült.Veya widgetlar ile yapilir.https://docs.djangoproject.com/en/4.0/ref/forms/widgets/
{% load crispy_forms_tags %}
    <form method="POST" enctype="multipart/form-data">   
      {% csrf_token %} {{form|crispy}}
      <br />
      <button type="submit" class="btn btn-outline-info">Post</button>
    </form>

pip freeze > ./requirements.txt

# 3rd part app ler belli bir grup tarafindan mesela django restframeworkü iyilestirmek icin disaridan yazilan paketler.pillow pythonun icinde olan bir kütürhane bunu import etmeye gerek yok.  
# -------------------------------------------------------------
# update.html 
{% extends 'base.html' %} {% load crispy_forms_tags %} {% block content %}
<div class="row">
  <div class="col-md-6 offset-md-3">
    <h3>Update Post</h3>
    <hr />
    <form method="POST" enctype="multipart/form-data">
      {% csrf_token %} {{form|crispy}}
      <br />
      <button type="submit" class="btn btn-outline-info">Update</button>
    </form>
  </div>
</div>

{% endblock content %}
# -------------------------------------------------------------
# delete.html

{% extends 'base.html' %} {% load static %} {% block content %}

<div class="row mt-5">
  <div class="col-md-6">
    <div class="card card-body">
      <p>Are you sure you want to delete "{{object}}"?</p>

      <form action=" " method="POST">
        {% csrf_token %}
        <a class="btn btn-warning" href="{% url 'blog:list' %}">Cancel</a>
        <input class="btn btn-danger" type="submit" name="Confirm" />
      </form>
    </div>
  </div>
</div>
{% endblock %}

# -------------------------------------------------------------
# USER APPLICATION
# user üzerinden profile modelini olusturalim, profile page icin formu olusturalim. Yeni bir app olusturuyoruz.
# py manage.py startapp users 
INSTALLED_APPS = [
    'users',
]
# hata alirsak su seklide de app eklenebilir
    # 'blog.apps.BlogConfig',
    # 'users.apps.UsersConfig',

# Bir user in bir profile i olmasi gerekiyor. Birden fazla profile i olamaz. one to one relation olmasi lazim. 

# models.py
from django.db import models
from django.contrib.auth.models import User

# upload icin alttaki fonksiyonu yazdik. Düzenli bir sekilde kaydetsin diye. Kullanicidan alinan bütün resimler veya videolar benim media_root un altina otomatik olarak gidecek. Django settingste belirledigimiz icin MEDIA_ROOT = BASE_DIR / "media_root" , otomatik bu klaör altina kaydedilir. Ama bu klasörün altinda bütün resimleri kimin yükledigi belli olmadan kaydedemem.Bundan dolayi blogtan gelen resimleri otomatik olarak blog altina user dan gelen resimleri user altina kaydeder. Blog ve User klasörlerini kendi olusturur. Ve id lere göre klasör olusturur ve id ler altina resimleri kaydeder.  
def user_profile_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.user.id, filename)
# {0} id yi {1} ise dosya ismini ifade ediyor.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= user_profile_path, default="avatar.png")
    bio = models.TextField(blank=True)

    def __str__(self):
        return "{} {}".format(self.user, 'Profile')    

python manage.py makemigrations
python manage.py migrate

# admin panele kaydet
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)

# User register oldugu zaman otomatik olarak profile i da olsun istiyorum. Gidip bir de profil yazmak istemiyorum. signals ne yapiyordu, post_save , pre_save , post_delete , pre_delete yapiyordu. Simdi sunu diyorum user olusturduktan sonra bir signal gönder ve profile i olustursun.

# signals.py
# post_save i import ettim
from django.db.models.signals import post_save
# user i import ettim
from django.contrib.auth.models import User
# reciver import etmem gerekiyor
from django.dispatch import receiver
# profile modeline de ihtiyacim olacak
from .models import Profile

# iki parametre alir. hangi method ve sender ne ? created demek user create edildiyse demek. **kwargs yazmak zorundasin cünkü django otomatik bazi seyleri kendisi koyuyor. Onlari karsilamak icin **kwargs koyuluyor.Normal bir sayfaya üye oldugumuz zaman bizim profile page i miz otomatik olarak gelir. Siz o profile sayfasina resim yüklersiniz. Ne eklnecekse onlar eklenir. Signals burada devreye giriyor. 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) 

# apps.py i da güncelle signals den sonra
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        import users.signals
    
 
# -------------------------------------------------------------
# ana urls.py dan yol verdim
urlpatterns = [
    path('users/', include('users.urls')),
]

# simdi users icindeki url ye gidelim.
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
# Yukarudaki name leri bu sekilde yazmamiz gerekiyor. 
# https://docs.djangoproject.com/en/4.0/topics/auth/default/

# REGISTER
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

# django bana default olarak bu view i verdi. as_view eklemek gerekiyor.name kesinlikle register olmak zorunda. template_name i user altina yönlendirmemiz gerekiyor.
    path("register/", register, name="register"),
]
# simdi forms.py yazalim. Django bana default olarak UserCreationForm veriyor. django/auth/forms.py altinda. Bu formda username , pass1 ve pass2 var. Ben buna e-mail ekleyecegim. Sifremi unuttum a tiklayinca e maile mesaj gidecek böyle oldugu icin email i benim zorunlu girilebilir ve uniq bir deger haline getirmem lazim. User register olurken e maili de girmesi gereksin.
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# UserCreationForm dan import ettim yani bütün özelliklerini inherit ettim. 
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()  #override ettik. boş bırakınca default required true oldu
    
    class Meta:
        model = User
# UserCreationForm da password vardi ben User modelimden e maili ve username i aldim.
        fields = ("username", "email")
        
# Form dan emaili cektk, daha önce db de var mi baktik.cleaned_data bu ise yarar.Djangoda bir field e cuntom validation yapacaksak clean_ yazip field ismi yazilir. 
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that one already taken")
        return email
    
# örnegin burada custom validation yaptik. Ismin icinde a varsa uyar kabul etme dedik.
    # def clean_first_name(self):
    #     name = self.cleaned_data("first_name")
    #     if "a" in name:
    #         raise forms.ValidationError("Your name includes A")
    #     return name
        
# Simdi views e ekleyelim.
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages

def register(request):
    form = RegistrationForm(request.POST or None) 
    if request.user.is_authenticated:
        messages.warning(request, "You are already have an account!")
        return redirect("blog:list")
    if form.is_valid():
        form.save()
        name = form.cleaned_data["username"]
        messages.success(request, f"Account created for {name}")
        return redirect("login")  
                
    context = {
        "form" : form
    }
    return render(request, "users/register.html", context)

# hemen bir templates acalim ve altina register.html acalim. 
{% extends 'base.html' %} {% block title %}Register{% endblock %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <form action="" method="post">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Join Today</legend>
            {{ form|crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Sign Up</button>
        </div>
    </form>
    <div class="border-top pt-3">
        <small class="text-muted">
            Already have an account?<a class="ml-2" href="{% url 'login'  %}">Sign In</a>
        </small>
    </div>

</div>
{% endblock %}
# urls e ekleyelim
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    path("register/", register, name="register"),
]

# navbara register urlsini eklemeyi unutma.
 <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>

# Formsu güncelleyelim. Forms a email alani ekleyelim.
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.forms import fields
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()  #override ettik. boş bırakınca default required true oldu
    
    class Meta:
        model = User
        fields = ("username", "email")
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that one already taken")
        return email
    
    # def clean_first_name(self):
    #     name = self.cleaned_data("first_name")
    #     if "a" in name:
    #         raise forms.ValidationError("Your name includes A")
    #     return name

# PROFILE 
# Asagida iki form u birlestirdik.ProfileUpdateForm ve UserUpdateForm. Bunlari views de profile_page icin kullanacagim.
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("image", "bio")

class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("username", "email")

# views e gel
def profile(request):
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, instance=request.user.profile, files=request.FILES)
    
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your profile has been updated!")
        return redirect(request.path)
    
    context = {
        "u_form" : u_form,
        "p_form" : p_form    
    }
    return render(request, "users/profile.html", context)
# profile.html olustur. 
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <div class="media">
        <img class="rounded-circle account-img" src="{{ user.profile.image.url }}">
        <div class="media-body">
            <h2 class="account-heading">{{ user.username }}</h2>
            <p class="text-secondary">{{ user.email }}</p>
        </div>
    </div>
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Profile</legend>
            {{ u_form|crispy }}
            {{ p_form|crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Update</button>
        </div>
    </form>
</div>
{% endblock content %}

# urls e ekle 
    path("profile/", profile, name="profile"),
# navbara da ekle 
        <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>

# LOGIN 
# urls e login yaz.
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),

# django default olarak bir login.html veriyor. ama bu template_name = 'registrtion/login.html' . Bizim registration diye appimiz olmadigi icin biz burayi düzenleyecegiz. urls in icinde template_name="users/login.html" ifadeyi yazdik.

# login.html olusturalim 
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <div class="media">
        <img class="rounded-circle account-img" src="{{ user.profile.image.url }}">
        <div class="media-body">
            <h2 class="account-heading">{{ user.username }}</h2>
            <p class="text-secondary">{{ user.email }}</p>
        </div>
    </div>
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Profile</legend>
            {{ u_form|crispy }}
            {{ p_form|crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Update</button>
        </div>
    </form>
</div>
{% endblock content %}

# Navbara login i bagla
        <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>

# Login icin son asama. default olarak baska bir adrese redirect eder. Ayarlara gel ve asagidaki kodu yaz.
LOGIN_REDIRECT_URL = "blog:list"
LOGIN_URL = "login"


# LOGOUT
# logout html de cok bir sey yazmamiza gerek yok django cogu seyi kendi yapiyor.
# logout.html
{% extends 'base.html' %} {% block title %}login{% endblock %}
{% block content %}
<h2>You have been logged out</h2>
<div class="border-top pt-3">
    <small class="text-muted">
        <a href="{% url 'login' %}">Log in Again</a>
    </small>
</div>

{% endblock %}

# normalde logout.vies yazilabilir ama gerek yok 
# urls e ekle 
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),

# djangoda login olmadan da create yapmayi engellemek icin views e gelip @login_required() koyulur, bunlara decorater denir.

# base.url ye messages ekle. her sayfaya tek tek eklemek yerine sadece base e ekle.
      <div class="container">
        {% if messages %}
        {% for message in messages %}

        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>

        {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </div>

# user coktan login olduysa register sayfasina ulassin istemiyorum. Normalde navbarda bunu ayarlamistim. Fakat manuel olarak register yazarsam arama cubuguna bu beni yine de register sayfasina yönlendiriyor. Bunu engellemem lazim. views e sunu ekle.
if request.user.is_authenticated:
        messages.warning(request, "You are already have an account!")
        return redirect("blog:list")
# Bu da account olusturulmussa gönderilecek mesaj 
    if form.is_valid():
        form.save()
        name = form.cleaned_data["username"]
        messages.success(request, f"Account created for {name}")
        return redirect("login")  
# Profil update edilmissi 
if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your profile has been updated!")
        return redirect(request.path)

# PASSWORD RESET EMAIL
# urls e ekleyerek basla
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="users/password_reset_email.html", form_class=PasswordResetEmailCheck), name="password_reset"),

# password_reset_email.html olustur 
{% extends 'base.html' %} {% block title %}login{% endblock %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <form action="" method="post">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Reset Password</legend>
            {{ form|crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Request Reset</button>
        </div>
    </form>

</div>
{% endblock %}

# PASSWORD RESET DONE
# urls e ekle 
PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
# password_reset_done.html olustur 
{% extends 'base.html' %} {% block title %}login{% endblock %}
{% block content %}
<div class="alert alert-info">
    <p>We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You
        should receive them shortly.</p>

    <p>If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your
        spam folder.</p>
</div>

{% endblock %}

# PASSWORD RESET CONFIRM DONE 
# urls e ekle 
    path("password-reset-confirm/<uuidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),

# password_reset_confirm.html olustur
{% extends 'base.html' %} {% block title %}login{% endblock %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <form action="" method="POST">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Reset Password</legend>
            {{ form|crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Reset Password</button>
        </div>
    </form>

</div>
{% endblock %}

# PASSWORD RESET COMPLETE
# urls yaz ekle
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),

# password_reset_complete.html olustur
{% extends 'base.html' %} {% block title %}login{% endblock %}
{% block content %}
<div class="alert alert-info">
    Your password has been set successfully!
</div>
<a href="{% url 'login' %}">Sign In Here</a>

{% endblock %}

# SETTINGS . gmail e git denemek icin sunu yap. Google Hesabinizi Yönetin > Güvenlik > Daha az güvenli uygulamaya erisim diye bir yer var. Onu acik yap.
#Sending email (gmail ayarlardan uygulamaya izin ver!)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")

