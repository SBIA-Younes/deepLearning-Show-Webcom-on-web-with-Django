from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse 

class BlogPost(models.Model):
  
  class Meta:
    verbose_name = _('article')
    verbose_name_plural = _('articles')
    ordering = ["-created_on"]
    
  title = models.CharField(max_length=255, verbose_name=_('Titre'))
  
  slug = models.SlugField(max_length=255,unique=True,blank=True,verbose_name=_("SLug"))
  
  image = models.ImageField(upload_to="Content/images/%Y/%m/%d/",verbose_name=_("Image"),null=True,blank=True)
  
  content = models.TextField(verbose_name=_('Contenu'))
  
  
  last_update = models.DateTimeField(auto_now=True,verbose_name=_("Dernière Modification"))
  
  created_on = models.DateField(auto_now_add=True,null=True, blank=True,verbose_name=_("Creation à"))
  
  published = models.BooleanField(default=False, verbose_name=_("Publié"))
  
  internet = models.BooleanField(default=False, verbose_name=_("internet"))
  
  
  # def get_absolute_url(self):
  #     return reverse("article-detail", kwargs={"slug": self.slug})
  
  def __str__(self):
      return self.title
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
      
    super().save(*args, **kwargs)

