from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Extended, Movie


class SuperAdmin(admin.ModelAdmin):
    list_display = ('title', 'released', 'director', 'writer')
    list_filter = ('genre', 'released', 'rated')
    search_fields = ('title', 'plot')
    # fields = (('title', 'released'), 'plot', ('writer', 'director'), 'rated')
    # exclude = ('writer', 'director')

    fieldsets = (
        ('Basic Information', {
            'fields': (('title', 'released'), ('rated', 'director'), ('writer', 'genre'))
        }),
        ('More Information', {
            'classes': ('collapse',),
            'fields': ('plot', 'actors', 'language', 'country', 'type')
        }),
    )


# Register your models here.
admin.site.register(Student)
admin.site.register(Extended)
admin.site.register(Movie, SuperAdmin)