from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Exam(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    total_marks = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=30)
    passing_marks = models.PositiveIntegerField(default=0)
    attempt_limit = models.PositiveIntegerField(default=1)

    subject_ref = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    instructions = models.TextField(blank=True, null=True)
    exam_code = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text[:50]


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0)
    pass_status = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"


class StudentAnswer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        blank=True,
        null=True
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.result.student.username} - {self.question.id}"


class ExamAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    attempt_number = models.PositiveIntegerField(default=1)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam', 'attempt_number')

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} - Attempt {self.attempt_number}"


class Announcement(models.Model):
    AUDIENCE_CHOICES = (
        ('all', 'All'),
        ('students', 'Students'),
        ('teachers', 'Teachers'),
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title