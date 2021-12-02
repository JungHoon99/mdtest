from django.contrib import admin

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    fileds = ['pub_date', 'question_text']

admin.site.register(Question)
# Register your models here.
