# Virtual enviroment olusturuyoruz. Sonra activate ediyoruz 
py -m venv benv 
source ./env/Scripts/activate
# Django yüklenir.  
pip install django
# Sonrasinda decouple ve pillow yüklenir. 
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


# Djangonun boze otomatik verdigi bir user modeli var.Öncelikle ondanbahsedelim. 
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
    
    class Meta:
        verbose_name_plural = "Categories"
        
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

# Bir "slug", genellikle önceden elde edilmiş verileri kullanarak geçerli bir URL oluşturmanın bir yoludur. Örneğin, bir bilgi, bir URL oluşturmak için bir makalenin başlığını kullanır. Slug'u manuel olarak ayarlamak yerine, başlık (veya başka bir veri parçası) verilen bir işlev aracılığıyla oluşturmanızı tavsiye ederim.Aralara - koyarak URL olusturur. slug how-to-learn-django
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title
    
    
    
    def comment_count(self):
        return self.comment_set.all().count()
    
    def view_count(self):
        return self.postview_set.all().count()
    
    def like_count(self):
        return self.like_set.all().count()
    
    def comments(self):
        return self.comment_set.all()

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
    
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    

