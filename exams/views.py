from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Count
from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, Question, Result, StudentAnswer, ExamAttempt
from .forms import ExamForm, QuestionForm
from accounts.views import teacher_required, student_required


@login_required
def exam_list(request):
    exams = Exam.objects.filter(
        is_active=True, is_published=True).order_by('-created_at')
    query = request.GET.get('q')
    subject = request.GET.get('subject')

    if query:
        exams = exams.filter(title__icontains=query)
    if subject:
        exams = exams.filter(subject__icontains=subject)

    subjects = Exam.objects.values_list('subject', flat=True).distinct()
    return render(request, 'exams/exam_list.html', {
        'exams': exams,
        'subjects': subjects,
    })


@login_required
@teacher_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            messages.success(request, 'Exam created successfully.')
            return redirect('exam_detail', pk=exam.id)
    else:
        form = ExamForm()
    return render(request, 'exams/exam_form.html', {'form': form, 'page_title': 'Create Exam'})


@login_required
@teacher_required
def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully.')
            return redirect('exam_detail', pk=exam.id)
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exams/exam_form.html', {'form': form, 'page_title': 'Update Exam'})


@login_required
@teacher_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully.')
        return redirect('exam_list')
    return render(request, 'exams/confirm_delete.html', {'object': exam, 'type': 'Exam'})


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.questions.all()
    attempts_used = 0
    attempts_left = exam.attempt_limit

    if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
        attempts_used = Result.objects.filter(
            student=request.user, exam=exam).count()
        attempts_left = max(0, exam.attempt_limit - attempts_used)

    return render(request, 'exams/exam_detail.html', {
        'exam': exam,
        'questions': questions,
        'attempts_used': attempts_used,
        'attempts_left': attempts_left,
    })


@login_required
@teacher_required
def question_create(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, teacher=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            exam.total_marks = sum(q.marks for q in exam.questions.all())
            exam.save()
            messages.success(request, 'Question added successfully.')
            return redirect('exam_detail', pk=exam.id)
    else:
        form = QuestionForm()
    return render(request, 'exams/question_form.html', {'form': form, 'exam': exam})


@login_required
@teacher_required
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk, exam__teacher=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            exam = question.exam
            exam.total_marks = sum(q.marks for q in exam.questions.all())
            exam.save()
            messages.success(request, 'Question updated successfully.')
            return redirect('exam_detail', pk=exam.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'exams/question_edit.html', {'form': form, 'question': question})


@login_required
@teacher_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk, exam__teacher=request.user)
    exam = question.exam
    if request.method == 'POST':
        question.delete()
        exam.total_marks = sum(q.marks for q in exam.questions.all())
        exam.save()
        messages.success(request, 'Question deleted successfully.')
        return redirect('exam_detail', pk=exam.id)
    return render(request, 'exams/confirm_delete.html', {'object': question, 'type': 'Question'})


@login_required
@student_required
def exam_instructions(request, exam_id):
    exam = get_object_or_404(
        Exam, id=exam_id, is_active=True, is_published=True)
    attempt_count = Result.objects.filter(
        student=request.user, exam=exam).count()
    attempts_left = exam.attempt_limit - attempt_count

    if attempts_left <= 0:
        messages.error(
            request, 'You have reached the attempt limit for this exam.')
        return redirect('exam_detail', pk=exam.id)

    return render(request, 'exams/exam_instructions.html', {
        'exam': exam,
        'attempts_left': attempts_left,
    })


@login_required
@student_required
def take_exam(request, exam_id):
    exam = get_object_or_404(
        Exam, id=exam_id, is_active=True, is_published=True)
    questions = exam.questions.all().order_by('?')

    attempt_count = Result.objects.filter(
        student=request.user, exam=exam).count()
    if attempt_count >= exam.attempt_limit:
        messages.error(request, 'Attempt limit exceeded for this exam.')
        return redirect('exam_detail', pk=exam.id)

    if request.method == 'POST':
        total = sum(q.marks for q in questions)
        score = 0
        result = Result.objects.create(
            student=request.user, exam=exam, total=total)
        ExamAttempt.objects.create(
            student=request.user,
            exam=exam,
            attempt_number=attempt_count + 1
        )
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            is_correct = selected == question.correct_option if selected else False

            StudentAnswer.objects.create(
                result=result,
                question=question,
                selected_option=selected if selected else None,
                is_correct=is_correct
            )

            if is_correct:
                score += question.marks

        result.score = score
        result.percentage = round((score / total * 100), 2) if total > 0 else 0
        result.pass_status = score >= exam.passing_marks
        result.save()

        return redirect('result_detail', pk=result.id)

    return render(request, 'exams/take_exam.html', {'exam': exam, 'questions': questions})


@login_required
def result_detail(request, pk):
    result = get_object_or_404(Result, pk=pk)

    if hasattr(request.user, 'profile') and request.user.profile.role == 'student' and result.student != request.user:
        messages.error(request, 'You are not allowed to view this result.')
        return redirect('result_list')

    answers = result.answers.select_related('question')
    return render(request, 'exams/result_detail.html', {'result': result, 'answers': answers})


@login_required
def result_list(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
        results = Result.objects.filter(
            student=request.user).order_by('-submitted_at')
    else:
        results = Result.objects.all().order_by('-submitted_at')
    return render(request, 'exams/result_list.html', {'results': results})


@login_required
@teacher_required
def teacher_analytics(request):
    exams = Exam.objects.filter(teacher=request.user)
    total_exams = exams.count()
    total_questions = Question.objects.filter(
        exam__teacher=request.user).count()
    total_results = Result.objects.filter(exam__teacher=request.user).count()

    stats = Result.objects.filter(exam__teacher=request.user).aggregate(
        avg_score=Avg('percentage'),
        max_score=Max('percentage')
    )

    exam_stats = exams.annotate(student_count=Count('result'))

    return render(request, 'accounts/dashboard.html', {
        'profile': request.user.profile,
        'analytics': True,
        'total_exams': total_exams,
        'total_questions': total_questions,
        'total_results': total_results,
        'avg_score': stats['avg_score'] or 0,
        'max_score': stats['max_score'] or 0,
        'exam_stats': exam_stats,
    })
