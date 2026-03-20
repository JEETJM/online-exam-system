
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
        is_active=True,
        is_published=True
    ).order_by('-created_at')

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


# @login_required
# @teacher_required
# def exam_create(request):
#     if request.method == 'POST':
#         form = ExamForm(request.POST)
#         if form.is_valid():
#             exam = form.save(commit=False)
#             exam.teacher = request.user
#             exam.save()
#             messages.success(request, 'Exam created successfully.')
#             return redirect('exam_detail', pk=exam.id)
#     else:
#         form = ExamForm()

#     return render(request, 'exams/exam_form.html', {
#         'form': form,
#         'page_title': 'Create Exam'
#     })









@login_required
@teacher_required
def exam_create(request):
    print("METHOD:", request.method)

    if request.method == 'POST':
        print("POST DATA:", request.POST)

        form = ExamForm(request.POST)

        if form.is_valid():
            print("FORM VALID")
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            print("EXAM SAVED:", exam.id)
            messages.success(request, 'Exam created successfully.')
            return redirect('exam_detail', pk=exam.id)
        else:
            print("FORM INVALID")
            print(form.errors)

    else:
        form = ExamForm()

    return render(request, 'exams/exam_form.html', {
        'form': form,
        'page_title': 'Create Exam'
    })
    
    
    
    

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

    return render(request, 'exams/exam_form.html', {
        'form': form,
        'page_title': 'Update Exam'
    })


@login_required
@teacher_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)

    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully.')
        return redirect('exam_list')

    return render(request, 'exams/confirm_delete.html', {
        'object': exam,
        'type': 'Exam'
    })


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

    return render(request, 'exams/question_form.html', {
        'form': form,
        'exam': exam
    })


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

    return render(request, 'exams/question_edit.html', {
        'form': form,
        'question': question
    })


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

    return render(request, 'exams/confirm_delete.html', {
        'object': question,
        'type': 'Question'
    })


@login_required
@student_required
def exam_instructions(request, exam_id):
    exam = get_object_or_404(
        Exam,
        id=exam_id,
        is_active=True,
        is_published=True
    )

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
        Exam,
        id=exam_id,
        is_active=True,
        is_published=True
    )

    # Randomize question support if field exists
    if hasattr(exam, 'randomize_questions') and exam.randomize_questions:
        questions = exam.questions.all().order_by('?')
    else:
        questions = exam.questions.all()

    attempt_count = Result.objects.filter(
        student=request.user, exam=exam).count()

    if attempt_count >= exam.attempt_limit:
        messages.error(request, 'Attempt limit exceeded for this exam.')
        return redirect('exam_detail', pk=exam.id)

    if request.method == 'POST':
        total = sum(float(q.marks) for q in questions)
        score = 0.0

        result = Result.objects.create(
            student=request.user,
            exam=exam,
            total=total
        )

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
                score += float(question.marks)
            elif hasattr(exam, 'negative_marking') and exam.negative_marking and selected:
                negative_value = float(
                    getattr(exam, 'negative_marks_per_wrong', 0) or 0)
                score -= negative_value

        score = max(score, 0.0)

        result.score = score
        result.total = total
        result.percentage = round((score / total * 100), 2) if total > 0 else 0

        passing_marks = float(exam.passing_marks or 0)
        result.pass_status = score >= passing_marks

        result.save()

        return redirect('result_detail', pk=result.id)

    return render(request, 'exams/take_exam.html', {
        'exam': exam,
        'questions': questions
    })


@login_required
def result_detail(request, pk):
    result = get_object_or_404(Result, pk=pk)

    if (
        hasattr(request.user, 'profile')
        and request.user.profile.role == 'student'
        and result.student != request.user
    ):
        messages.error(request, 'You are not allowed to view this result.')
        return redirect('result_list')

    answers = result.answers.select_related('question')

    return render(request, 'exams/result_detail.html', {
        'result': result,
        'answers': answers
    })


@login_required
def result_list(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
        results = Result.objects.filter(
            student=request.user).order_by('-submitted_at')
    else:
        results = Result.objects.all().order_by('-submitted_at')

    return render(request, 'exams/result_list.html', {
        'results': results
    })


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


@login_required
def books_page(request):
    books = [
        {
            "title": "Python Programming Handbook",
            "subject": "Python",
            "desc": "Core concepts, syntax, MCQ prep, functions, OOP, and practice notes.",
            "type": "PDF Notes",
            "level": "Beginner to Intermediate",
        },
        {
            "title": "Database Management System Notes",
            "subject": "DBMS",
            "desc": "ER model, normalization, SQL, transactions, and repeated exam topics.",
            "type": "Theory + MCQ",
            "level": "Semester Prep",
        },
        {
            "title": "Operating System Revision Guide",
            "subject": "OS",
            "desc": "Process, scheduling, memory management, deadlock, and short questions.",
            "type": "Revision Sheet",
            "level": "Exam Ready",
        },
        {
            "title": "Computer Networks Quick Notes",
            "subject": "CN",
            "desc": "OSI model, TCP/IP, routing, switching, protocols, and viva questions.",
            "type": "Short Notes",
            "level": "Fast Revision",
        },
        {
            "title": "Data Structures Complete Notes",
            "subject": "DSA",
            "desc": "Stack, queue, linked list, tree, graph, sorting, and complexity basics.",
            "type": "Concept Book",
            "level": "Practice Oriented",
        },
        {
            "title": "Software Engineering Essentials",
            "subject": "SE",
            "desc": "SDLC, testing, models, design basics, project flow, and important theory.",
            "type": "Exam Notes",
            "level": "University Use",
        },

        {"title": "Advanced Python Notes", "subject": "Python",
            "desc": "Decorators, generators, OOP deep concepts.", "type": "Notes", "level": "Advanced"},
        {"title": "DBMS Complete Guide", "subject": "DBMS",
            "desc": "Normalization, SQL, transactions.", "type": "PDF", "level": "Intermediate"},
        {"title": "Operating System Concepts", "subject": "OS",
            "desc": "Process, memory, scheduling.", "type": "Theory", "level": "Core"},
        {"title": "Computer Networks Basics", "subject": "CN",
            "desc": "OSI, TCP/IP, protocols.", "type": "Notes", "level": "Beginner"},
        {"title": "Data Structures in C", "subject": "DSA",
            "desc": "Stack, Queue, Linked List.", "type": "Practice", "level": "Core"},
        {"title": "Java Programming", "subject": "Java",
            "desc": "OOP, multithreading, collections.", "type": "PDF", "level": "Intermediate"},
        {"title": "Software Engineering", "subject": "SE",
            "desc": "SDLC, Agile, Testing.", "type": "Notes", "level": "Exam"},
        {"title": "Web Development Basics", "subject": "Web",
            "desc": "HTML, CSS, JS fundamentals.", "type": "Guide", "level": "Beginner"},
        {"title": "Django Full Guide", "subject": "Django",
            "desc": "Models, views, templates.", "type": "Framework", "level": "Intermediate"},
        {"title": "Machine Learning Intro", "subject": "ML",
            "desc": "Supervised & unsupervised learning.", "type": "PDF", "level": "Basic"},
        {"title": "Artificial Intelligence", "subject": "AI",
            "desc": "Search, reasoning, ML basics.", "type": "Theory", "level": "Intermediate"},
        {"title": "Cyber Security Basics", "subject": "Security",
            "desc": "Encryption, attacks, defense.", "type": "Guide", "level": "Beginner"},
        {"title": "Cloud Computing", "subject": "Cloud",
            "desc": "AWS, Azure basics.", "type": "Notes", "level": "Intermediate"},
        {"title": "Linux Essentials", "subject": "OS",
            "desc": "Commands, shell scripting.", "type": "Practice", "level": "Beginner"},
        {"title": "C Programming", "subject": "C",
            "desc": "Pointers, memory, basics.", "type": "PDF", "level": "Core"},
        {"title": "C++ OOP Concepts", "subject": "C++",
            "desc": "Classes, inheritance, polymorphism.", "type": "Notes", "level": "Intermediate"},
        {"title": "Digital Electronics", "subject": "DE",
            "desc": "Logic gates, circuits.", "type": "Theory", "level": "Core"},
        {"title": "Compiler Design", "subject": "CD",
            "desc": "Parsing, lexical analysis.", "type": "Advanced", "level": "Advanced"},


    ]

    return render(request, 'exams/books.html', {
        'books': books
    })


@login_required
def pyq_page(request):
    pyqs = [
        {
            "title": "Python PYQ 2024",
            "subject": "Python",
            "year": "2024",
            "desc": "Important MCQs, output questions, and practical-oriented repeated patterns.",
            "paper_type": "Previous Year Paper",
        },
        {
            "title": "DBMS PYQ 2023",
            "subject": "DBMS",
            "year": "2023",
            "desc": "Normalization, SQL queries, transaction-based descriptive and short questions.",
            "paper_type": "University Questions",
        },
        {
            "title": "Operating System PYQ 2022",
            "subject": "OS",
            "year": "2022",
            "desc": "Process scheduling, paging, deadlock, synchronization, and long-answer topics.",
            "paper_type": "Semester Paper",
        },
        {
            "title": "Computer Networks PYQ 2021",
            "subject": "CN",
            "year": "2021",
            "desc": "Layer-based theory, routing algorithms, switching, and short viva questions.",
            "paper_type": "Final Exam Paper",
        },
        {
            "title": "Software Engineering PYQ 2023",
            "subject": "SE",
            "year": "2023",
            "desc": "SDLC, testing, design models, requirement engineering, and software lifecycle.",
            "paper_type": "Question Bank",
        },
        {
            "title": "Data Structures PYQ 2024",
            "subject": "DSA",
            "year": "2024",
            "desc": "Array, stack, queue, tree, graph, searching, sorting, and algorithm basics.",
            "paper_type": "Important Set",
        },
    ]

    return render(request, 'exams/pyq.html', {
        'pyqs': pyqs
    })


@login_required
def support_page(request):
    support_items = [
        {
            "title": "Exam Guidelines",
            "icon": "bi-shield-check",
            "desc": "Read all important rules before starting any online examination.",
        },
        {
            "title": "Student Help Desk",
            "icon": "bi-headset",
            "desc": "Get support for login issues, exam access problems, and submission doubts.",
        },
        {
            "title": "Download Resources",
            "icon": "bi-download",
            "desc": "Access useful PDFs, revision sheets, sample patterns, and academic support files.",
        },
        {
            "title": "Teacher Support",
            "icon": "bi-person-workspace",
            "desc": "Teachers can manage exams, add questions, and review student performance.",
        },
        {
            "title": "Technical Help",
            "icon": "bi-tools",
            "desc": "Troubleshoot browser, device, internet, and dark mode related issues.",
        },
        {
            "title": "Academic FAQ",
            "icon": "bi-patch-question",
            "desc": "Get answers to common questions about exams, attempts, results, and resources.",
        },
    ]

    return render(request, 'exams/support.html', {
        'support_items': support_items
    })
