from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, QuizAttempt
from .forms import QuizForm, QuestionForm, AnswerForm
from django.contrib import messages


@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, created_by=request.user)
    
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz został usunięty.')
        return redirect('quizzes:quiz_list')
    
    return render(request, 'quizzes/confirm_delete_quiz.html', {'quiz': quiz})


@login_required
def edit_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id, quiz_id=quiz_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('quizzes:edit_quiz', quiz_id=quiz_id)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'quizzes/edit_question.html', {
        'form': form,
        'question': question,
        'quiz_id': quiz_id,
    })


@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, created_by=request.user)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz)
        question_form = QuestionForm(request.POST)
        answer_form = AnswerForm(request.POST)

        if quiz_form.is_valid():
            quiz_form.save()

        if 'add_question_with_answers' in request.POST:
            if question_form.is_valid() and answer_form.is_valid():
                new_question = question_form.save(commit=False)
                new_question.quiz = quiz
                new_question.save()
                
                for letter in ['A', 'B', 'C', 'D']:
                    Answer.objects.create(
                        question=new_question,
                        text=answer_form.cleaned_data[f'text_{letter}'],
                        is_correct=answer_form.cleaned_data[f'is_correct_{letter}'],
                        letter=letter
                    )
                messages.success(request, 'Pytanie i odpowiedzi zostały dodane.')
                return redirect('quizzes:edit_quiz', quiz_id=quiz.id)

        elif 'add_answers_to_question' in request.POST:
            question_id = request.POST.get('question_id')
            if question_id and answer_form.is_valid():
                question = get_object_or_404(Question, pk=question_id)
                
                # Najpierw usuń wszystkie istniejące odpowiedzi dla tego pytania
                question.answers.all().delete()
                
                # Następnie dodaj nowe odpowiedzi
                for letter in ['A', 'B', 'C', 'D']:
                    Answer.objects.create(
                        question=question,
                        text=answer_form.cleaned_data[f'text_{letter}'],
                        is_correct=answer_form.cleaned_data[f'is_correct_{letter}'],
                        letter=letter
                    )
                messages.success(request, 'Odpowiedzi zostały zaktualizowane.')
                return redirect('quizzes:edit_quiz', quiz_id=quiz.id)

    else:
        quiz_form = QuizForm(instance=quiz)
        question_form = QuestionForm()
        answer_form = AnswerForm()

    questions = quiz.questions.all()

    return render(request, 'quizzes/edit_quiz.html', {
        'quiz_form': quiz_form,
        'question_form': question_form,
        'answer_form': answer_form,
        'quiz': quiz,
        'questions': questions,
    })

@login_required
def delete_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, created_by=request.user)
    question = get_object_or_404(Question, pk=question_id, quiz=quiz)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Pytanie zostało usunięte.')
        return redirect('quizzes:edit_quiz', quiz_id=quiz.id)
    
    return render(request, 'quizzes/confirm_delete_question.html', {'question': question, 'quiz': quiz})

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

# quizzes/views.py
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    is_owner = request.user == quiz.created_by  # Sprawdź czy użytkownik jest właścicielem
    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'is_owner': is_owner,
    })
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__answers'), pk=quiz_id)
    
    if request.method == 'POST':
        score = 0
        total_questions = quiz.questions.count()
        user_answers = {}
        correct_answers = {}  # Nowy słownik dla poprawnych odpowiedzi
        
        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')
            user_answers[str(question.id)] = selected_answer_id
            
            # Znajdź poprawną odpowiedź dla każdego pytania
            correct_answer = question.answers.filter(is_correct=True).first()
            if correct_answer:
                correct_answers[str(question.id)] = correct_answer.id
            
            if selected_answer_id:
                answer = Answer.objects.get(id=int(selected_answer_id))
                if answer.is_correct:
                    score += 1
        
        return render(request, 'quizzes/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': total_questions,
            'percentage': int((score / total_questions) * 100) if total_questions > 0 else 0,
            'user_answers': user_answers,
            'correct_answers': correct_answers  # Przekazujemy poprawne odpowiedzi
        })
    
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz})
@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('quizzes:add_questions', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'form': form})

@login_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_form = AnswerForm(request.POST)
        
        if question_form.is_valid() and answer_form.is_valid():
            # Save question
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            # Save answers A-D
            for letter in ['A', 'B', 'C', 'D']:
                Answer.objects.create(
                    question=question,
                    text=answer_form.cleaned_data[f'text_{letter}'],
                    is_correct=answer_form.cleaned_data[f'is_correct_{letter}'],
                    letter=letter
                )
            return redirect('quizzes:add_questions', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()
        answer_form = AnswerForm()
    
    return render(request, 'quizzes/add_questions.html', {
        'quiz': quiz,
        'question_form': question_form,
        'answer_form': answer_form,
        'questions': quiz.questions.all()
    })

def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quizzes/quiz_result.html', {'quiz': quiz})

@login_required
def finish_quiz_creation(request, quiz_id):
    return redirect('quizzes:quiz_detail', quiz_id=quiz_id)