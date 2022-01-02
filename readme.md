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
        instance.slug = slugify(instance.title + " " + get_random_code())
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
# Postun icindeki options lari dogrudan burada da kullanabiliriz
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
    <form method="POST" enctype="multipart/form-data">   
      {% csrf_token %} {{form|crispy}}
      <br />
      <button type="submit" class="btn btn-outline-info">Post</button>
    </form>
  </div>
</div>

{% endblock content %}
# -------------------------------------------------------------


