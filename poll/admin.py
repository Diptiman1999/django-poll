from django.contrib import admin

from .models import Question,Choice
# Register your models here.

# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_Date', 'question_text']
#This will make the publication date to come first followed by question_text

class ChoiceInline(admin.StackedInline):#Stacked Line tells it will one after another
# With that TabularInline (instead of StackedInline), the related objects are displayed in a more compact, table-based format
#it will have an extra delte columns
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_Date'], 'classes': ['collapse']}),#Collapse is used thide it or show it
    ]
    inlines = [ChoiceInline]
    #Here fieldsets is list containing tuples where first vale of the tuple represents  Heaing followed by fielsd which is a dictionary
    # fieldsets , fields and inline are predifined words
    list_display = ('question_text', 'pub_Date', 'was_published_recently')#Used to show the question in list view
    list_filter = ['pub_Date']#Because pub_date is a DateTimeField, Django knows to give appropriate filter options: “Any date”, “Today”, “Past 7 days”, “This month”, “This year”
    


admin.site.register(Question, QuestionAdmin)
