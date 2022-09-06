from django.contrib import admin
from .models import *

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    readonly_fields = ('entry_date',)


admin.site.register(Expense, ExpenseAdmin)

admin.site.register(Categories)
admin.site.register(SignUp)
admin.site.register(Contact)
admin.site.register(Subscribe)
admin.site.register(Faqs)