from django.contrib import admin

from document_management.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    # def has_delete_permission(self, request, obj=None):
    #     # Disable delete permission for documents
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     # Disable edit permission for documents
    #     return False