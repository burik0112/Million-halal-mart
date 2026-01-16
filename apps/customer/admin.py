from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display=['start_date','title', 'end_date', 'description']
class ProfileAdmin(admin.ModelAdmin):
    list_display=['phone_number','full_name', 'created']
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location)
admin.site.register(News, NewsAdmin)
admin.site.register(ViewedNews)
admin.site.register(Favorite)
admin.site.register(Banner)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 1. Ro'yxatda ko'rinadigan ustunlar
    list_display = ('username', 'email', 'is_wholesaler', 'is_approved', 'is_staff')

    # 2. Yon tomondagi filtrlar
    list_filter = ('is_wholesaler', 'is_approved', 'is_staff', 'is_superuser')

    # 3. Foydalanuvchini tahrirlash sahifasida yangi maydonlarni qo'shish
    # Standard UserAdmin fieldsetlariga bizning maydonlarni qo'shamiz
    fieldsets = UserAdmin.fieldsets + (
        ('Optomchi Maqomi', {'fields': ('is_wholesaler', 'is_approved')}),
    )

    # 4. Yangi foydalanuvchi yaratish sahifasida ko'rinishi
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Optomchi Maqomi', {'fields': ('is_wholesaler', 'is_approved')}),
    )

    # 5. Admin panelning o'zidan turib tezkor tasdiqlash (Action)
    actions = ['approve_wholesalers', 'unapprove_wholesalers']

    @admin.action(description="Tanlanganlarni optomchi sifatida tasdiqlash")
    def approve_wholesalers(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} ta foydalanuvchi tasdiqlandi.")

    @admin.action(description="Tanlanganlardan optomchi maqomini olib tashlash")
    def unapprove_wholesalers(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} ta foydalanuvchidan tasdiq olib tashlandi.")
