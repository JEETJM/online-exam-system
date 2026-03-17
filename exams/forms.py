# from django import forms
# from .models import Exam, Question

# class ExamForm(forms.ModelForm):
#     class Meta:
#         model = Exam
#         fields = [
#             'title',
#             'subject',
#             'description',
#             'duration_minutes',
#             'passing_marks',
#             'attempt_limit',
#             'is_active',
#             'is_published',
#         ]
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4}),
#         }


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = [
#             'question_text',
#             'option_a',
#             'option_b',
#             'option_c',
#             'option_d',
#             'correct_option',
#             'marks',
#         ]
#         widgets = {
#             'question_text': forms.Textarea(attrs={'rows': 3}),
#         }


from django import forms
from .models import Exam, Question, SupportTicket


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'title',
            'subject',
            'subject_ref',
            'department',
            'semester',
            'description',
            'instructions',
            'duration_minutes',
            'passing_marks',
            'attempt_limit',
            'start_time',
            'end_time',
            'exam_code',
            'is_active',
            'is_published',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 4}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option',
            'marks',
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3}),
        }


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
