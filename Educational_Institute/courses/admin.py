from django.contrib import admin
from .models import Course, Prerequisite, Learning, Tag, Video, UserCourse , Payment 
# Register your models here.


class TagAdmin(admin.TabularInline):
    model = Tag

class LearningAdmin(admin.TabularInline):
    model = Learning

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite

class VideoAdmin(admin.TabularInline):
    model = Video   

class CourseAdmin(admin.ModelAdmin):
    inlines = [ TagAdmin , LearningAdmin , PrerequisiteAdmin , VideoAdmin ]
    list_display = ["name" , 'get_price' , "active"]
   
    def get_price(self , course):
        return f'₹ {course.price}'

    get_price.short_description="Price"

admin.site.register(Course , CourseAdmin)
admin.site.register(Video)
admin.site.register(Payment)
admin.site.register(UserCourse)


