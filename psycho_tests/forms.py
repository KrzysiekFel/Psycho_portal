from django import forms
from .models import PsychoTest, Question, Answer


class TestForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(),
                                               widget=forms.SelectMultiple(attrs={'class': 'select-list'}),
                                               required=False,
                                               help_text='(Optional): Choose questions from existing database.')

    custom_questions = forms.CharField(max_length=1000,
                                       required=False,
                                       widget=forms.Textarea,
                                       help_text='Enter up to 5 custom questions, each on a new line. Example:'
                                                 '"Mostly: 1.I am confident 2.I dont feel confident')

    answers = forms.CharField(max_length=500,
                              required=True,
                              widget=forms.Textarea,
                              help_text='Add your answers, each on a new line. Answers will be the same for all '
                                        'questions. Points for answers will be counted from zero for the first answer '
                                        'and then +1 for each next answer. E.g. if you give 3 answers (for example: '
                                        'rarely, I do not know, often) then the points will be sequentially set to 0, '
                                        '1, 2.')

    class Meta:
        model = PsychoTest
        fields = ['name', 'image', 'description', 'threshold', 'result_above_threshold', 'result_below_threshold',
                  'questions']
        help_texts = {
            'name': 'Test name.',
            'image': 'Add image, if not default will be added.',
            'description': 'What is your test about.',
            'threshold': 'Set a integer number which will be the threshold for two results.',
            'result_above_threshold': 'Description of test result when score is above or equal threshold.',
            'result_below_threshold': 'Description of test result when score is below threshold.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['questions'].widget.attrs.update({'class': 'checkbox-list'})
        self.fields['questions'].label_from_instance = lambda obj: obj.question_content

    def save(self, commit=True):
        test = super().save(commit=False)
        custom_questions = self.cleaned_data.get('custom_questions')
        answers = self.cleaned_data.get('answers')

        if commit:
            test.save()
            self.save_m2m()

        if custom_questions:
            custom_questions_list = custom_questions.split('\n')
            for custom_question_content in custom_questions_list:
                if custom_question_content:
                    question = Question.objects.create(question_content=custom_question_content)
                    test.questions.add(question)

        answers_list = answers.split('\n')
        for answer in answers_list:
            Answer.objects.create(answer=answer, psycho_test=test)

        return test


class TestFillForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        answers = kwargs.pop('answers')
        super().__init__(*args, **kwargs)

        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.question_content,
                choices=[(answer.pk, answer.answer) for answer in answers],
                widget=forms.RadioSelect
            )
