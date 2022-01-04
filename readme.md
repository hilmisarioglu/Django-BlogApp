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
# Like butonuna tekrar basarsam silinsin istiyorum. Bir de sunu kontrol edecegim, bu postun like i benim tarafimdan verilmis mi verilmemis mi? Eger daha önce verilmisse like i bir azaltack ilk defa verilmisse 1 artiracak. Yani bir kullanici sadece bir defa like verebilecek. 10 defa veremeyecek. 

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
54.03