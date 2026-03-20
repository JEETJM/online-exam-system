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


# from django import forms
# from .models import Exam, Question, SupportTicket


# class ExamForm(forms.ModelForm):
#     class Meta:
#         model = Exam
#         fields = [
#             'title',
#             'subject',
#             'subject_ref',
#             'department',
#             'semester',
#             'description',
#             'instructions',
#             'duration_minutes',
#             'passing_marks',
#             'attempt_limit',
#             'start_time',
#             'end_time',
#             'exam_code',
#             'is_active',
#             'is_published',
#         ]
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4}),
#             'instructions': forms.Textarea(attrs={'rows': 4}),
#             'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
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


# class SupportTicketForm(forms.ModelForm):
#     class Meta:
#         model = SupportTicket
#         fields = ['subject', 'message']
#         widgets = {
#             'message': forms.Textarea(attrs={'rows': 5}),
#         }
# 33333

# from django import forms
# from .models import Exam, Question, SupportTicket


# class ExamForm(forms.ModelForm):
#     class Meta:
#         model = Exam
#         fields = [
#             'title',
#             'subject',
#             'subject_ref',
#             'department',
#             'semester',
#             'description',
#             'instructions',
#             'duration_minutes',
#             'passing_marks',
#             'attempt_limit',
#             'start_time',
#             'end_time',
#             'exam_code',
#             'is_active',
#             'is_published',
#         ]
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'subject': forms.TextInput(attrs={'class': 'form-control'}),
#             'subject_ref': forms.TextInput(attrs={'class': 'form-control'}),
#             'department': forms.TextInput(attrs={'class': 'form-control'}),
#             'semester': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
#             'instructions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
#             'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
#             'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
#             'attempt_limit': forms.NumberInput(attrs={'class': 'form-control'}),
#             'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
#             'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
#             'exam_code': forms.TextInput(attrs={'class': 'form-control'}),
#         }


# class QuestionForm(forms.ModelForm):
#     question_text = forms.CharField(
#         label='Question Text',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
#     )
#     option_a = forms.CharField(
#         label='Option A',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#     )
#     option_b = forms.CharField(
#         label='Option B',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#     )
#     option_c = forms.CharField(
#         label='Option C',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#     )
#     option_d = forms.CharField(
#         label='Option D',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#     )
#     correct_option = forms.ChoiceField(
#         label='Correct Option',
#         choices=[
#             ('', '---------'),
#             ('A', 'A'),
#             ('B', 'B'),
#             ('C', 'C'),
#             ('D', 'D'),
#         ],
#         widget=forms.Select(attrs={'class': 'form-select'})
#     )
#     marks = forms.IntegerField(
#         label='Marks',
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#     )

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


# class SupportTicketForm(forms.ModelForm):
#     class Meta:
#         model = SupportTicket
#         fields = ['subject', 'message']
#         widgets = {
#             'subject': forms.TextInput(attrs={'class': 'form-control'}),
#             'message': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
#         }


from django import forms
from .models import Exam, Question, SupportTicket


class ExamForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    end_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )

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
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'attempt_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_code': forms.TextInput(attrs={'class': 'form-control'}),
            # 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'native-check',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'native-check',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class': 'form-select'})
        self.fields['subject_ref'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['department'].widget.attrs.update({'class': 'form-select'})
        self.fields['semester'].widget.attrs.update({'class': 'form-select'})

        self.fields['description'].required = False
        self.fields['instructions'].required = False


class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        label='Question Text',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    option_a = forms.CharField(
        label='Option A',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    option_b = forms.CharField(
        label='Option B',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    option_c = forms.CharField(
        label='Option C',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    option_d = forms.CharField(
        label='Option D',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    correct_option = forms.ChoiceField(
        label='Correct Option',
        choices=[
            ('', '---------'),
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    marks = forms.IntegerField(
        label='Marks',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

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


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
