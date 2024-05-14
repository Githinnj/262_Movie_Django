from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Movie,ReviewRating

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre')
    search_fields = ('title', 'genre')
    list_filter = ('release_date', 'genre')

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'text', 'rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'text')
    list_filter = ('created_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)