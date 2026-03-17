from django.contrib import admin
from .models import (
    Subject, Department, Exam, Question, Result,
    StudentAnswer, ExamAttempt, Announcement,
    SupportTicket, Notification
)

admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(StudentAnswer)
admin.site.register(ExamAttempt)
admin.site.register(Announcement)
admin.site.register(SupportTicket)
admin.site.register(Notification)