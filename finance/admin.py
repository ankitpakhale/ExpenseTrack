from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    readonly_fields = ('entry_date',)
    list_display = ('click_me','item', 'amount', 'date', 'is_delete')
    list_filter = ('date', 'category')
    list_per_page = 10
    def click_me(self, obj):
        return format_html(f'<a href="/admin/finantial_app/expense/{obj.id}/change/" class="default">View</a>')
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Categories)
admin.site.register(SignUp)
admin.site.register(Contact)
admin.site.register(Subscribe)
admin.site.register(Faqs)
