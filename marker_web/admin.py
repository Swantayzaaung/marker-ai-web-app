from django.contrib import admin
from .models import DownloadedPaper
# Register your models here.

@admin.register(DownloadedPaper)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ["id", "filename", "file"]
    list_editable = ["filename", "file"]

