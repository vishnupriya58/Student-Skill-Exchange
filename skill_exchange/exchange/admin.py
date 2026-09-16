from django.contrib import admin

from .models import (
    Skill,
    StudentSkill,
    StudentProfile,
    ExchangeRequest,
    Message,
    Session,
    Rating,
    Block,
    Report,
    Notification
)

admin.site.register(Skill)
admin.site.register(StudentSkill)
admin.site.register(StudentProfile)
admin.site.register(ExchangeRequest)
admin.site.register(Message)
admin.site.register(Session)
admin.site.register(Rating)
admin.site.register(Block)
admin.site.register(Report)
admin.site.register(Notification)