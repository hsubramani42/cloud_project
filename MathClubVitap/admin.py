from django.contrib import admin
from .models import *

class AdminMemberView(admin.ModelAdmin):
    list_display=['username','name','regno','type','tackle']
class AdminTempMemberView(admin.ModelAdmin):
    list_display=['username','password','name','regno']
class AdminView(admin.ModelAdmin):
    list_display=['username',"name"]
class AdminTackleMemberView(admin.ModelAdmin):
    model=Member
    list_display = ['get_member', 'file']
    def get_member(self, obj):
        return obj.member.regno
    get_member.admin_order_field='Member__regno'
class AdminFeedbackView(admin.ModelAdmin):
    def get_member(self, obj):
        return obj.member.regno
    model = Member
    get_member.admin_order_field = 'regno'
    list_display=['get_member','type','text','id']
class AdminTopscoresView(admin.ModelAdmin):
    def get_member(self, obj):
        return obj.member.regno
    model = Member
    get_member.admin_order_field = 'regno'
    list_display=['get_member',"score"]
class AdminMessageView(admin.ModelAdmin):
    def get_member(self, obj):
        return obj.member.regno
    model = Member
    get_member.admin_order_field = 'regno'
    list_display=['get_member',"name","message"]
class AdminEventView(admin.ModelAdmin):
    list_display=['username','regno',"slot","teamID","eventName"]
class AdminEvenCreatorView(admin.ModelAdmin):
    list_display=["eventName","description","team"]
class AdminFileView(admin.ModelAdmin):
    list_display=["name","file"]
admin.site.register(FileCSV,AdminFileView)
admin.site.register(Member,AdminMemberView)
admin.site.register(TempMember,AdminTempMemberView)
admin.site.register(Admin,AdminView)
admin.site.register(EventMember,AdminEventView)
admin.site.register(EventCreator,AdminEvenCreatorView)
admin.site.register(TackleMember,AdminTackleMemberView)
admin.site.register(Feedback,AdminFeedbackView)
admin.site.register(Message,AdminMessageView)
admin.site.register(Topscores,AdminTopscoresView)
