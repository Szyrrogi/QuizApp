import csv
from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question, Answer

class Command(BaseCommand):
    help = 'Importuje pytania i odpowiedzi z pliku CSV (automatycznie do pierwszego quizu)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ścieżka do pliku CSV')
        parser.add_argument(
            '--quiz-id',
            type=int,
            help='Opcjonalne ID quizu (jeśli pominięte, użyje pierwszego dostępnego)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        quiz_id = options['quiz_id']
        
        # Znajdź quiz
        if quiz_id:
            try:
                quiz = Quiz.objects.get(pk=quiz_id)
            except Quiz.DoesNotExist:
                self.stderr.write(f'Quiz o ID {quiz_id} nie istnieje!')
                return
        else:
            quiz = Quiz.objects.order_by('id').first()
            if not quiz:
                self.stderr.write('Brak dostępnych quizów! Najpierw utwórz quiz.')
                return
            self.stdout.write(f'Używam quizu o ID {quiz.id} ({quiz.title})')

        # Reszta kodu importu pozostaje bez zmian
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                question = Question.objects.create(
                    quiz=quiz,
                    text=row['question_text']
                )
                
                Answer.objects.create(
                    question=question,
                    text=row['answer_a'],
                    is_correct=row['correct_answer'].lower() == 'a',
                    letter='A'
                )
                Answer.objects.create(
                    question=question,
                    text=row['answer_b'],
                    is_correct=row['correct_answer'].lower() == 'b',
                    letter='B'
                )
                Answer.objects.create(
                    question=question,
                    text=row['answer_c'],
                    is_correct=row['correct_answer'].lower() == 'c',
                    letter='C'
                )
                Answer.objects.create(
                    question=question,
                    text=row['answer_d'],
                    is_correct=row['correct_answer'].lower() == 'd',
                    letter='D'
                )

        self.stdout.write(self.style.SUCCESS(f'Zaimportowano do quizu ID {quiz.id}'))