from django.contrib import admin
from .models import usuarios, posts, respuestas

# Pasamos al panel de admin las 2 tablas con las que trabajaremos por ahora
 
admin.site.register(usuarios)
admin.site.register(posts)
admin.site.register(respuestas)