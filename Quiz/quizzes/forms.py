from django import forms
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.Form):
    text_A = forms.CharField(label='Odpowiedź A', required=True)
    is_correct_A = forms.BooleanField(label='Poprawna?', required=False)
    text_B = forms.CharField(label='Odpowiedź B', required=True)
    is_correct_B = forms.BooleanField(label='Poprawna?', required=False)
    text_C = forms.CharField(label='Odpowiedź C', required=True)
    is_correct_C = forms.BooleanField(label='Poprawna?', required=False)
    text_D = forms.CharField(label='Odpowiedź D', required=True)
    is_correct_D = forms.BooleanField(label='Poprawna?', required=False)

    def clean(self):
        cleaned_data = super().clean()
        # Sprawdź czy przynajmniej jedna odpowiedź jest poprawna
        if not any([
            cleaned_data.get('is_correct_A'),
            cleaned_data.get('is_correct_B'),
            cleaned_data.get('is_correct_C'),
            cleaned_data.get('is_correct_D')
        ]):
            raise forms.ValidationError("Przynajmniej jedna odpowiedź musi być poprawna.")
        return cleaned_data