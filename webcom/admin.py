from django.contrib import admin
from .models import BlogPost
from django.utils.html import format_html


class BlogPostAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ("title",
                  # "created_on",
                  "published","internet",
                  "image_display"
                  )
  list_editable = ("published","internet")
  def image_display(self, obj):
      if obj.image:
          return format_html("<img src='{}' width='50' height='50' />".format(obj.image.url))
      else:
          return "Pas d'image"
admin.site.register(BlogPost, BlogPostAdmin)


