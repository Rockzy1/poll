from encodings import search_function
from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class ChoiceAdmin(admin.ModelAdmin):
    search_fields = ['question_text']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

