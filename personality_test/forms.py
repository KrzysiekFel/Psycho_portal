from django import forms
from .models import PersonalityTest, PsychoTest, Question


class PersonalityForm(forms.ModelForm):
    class Meta:
        model = PersonalityTest
        fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'question_7']
        help_texts = {
            'question_1': '1. Are generally sociable    2. Are generally quiet',
            'question_2': '1. Are focused on the outer world    2. Are focused on their inner world',
            'question_3': '1. Get energy by spending time with others   2. Get energy by spending time alone',
            'question_4': '1. Talk a lot & start conversations  2. Mostly listen & wait for others to talk first',
            'question_5': '1. Speak first, then think   2. Think first, then speak',
            'question_6': '1. Are quick to take action  2. Are slow to take action',
            'question_7': '1. Have many friends & many interests    2. Have a few deep friendships & refined interests',
        }


class TestForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(),
                                               widget=forms.SelectMultiple(attrs={'class': 'select-list'}),
                                               required=False,
                                               help_text='(Optional): Choose questions from existing database.')
    custom_questions = forms.CharField(max_length=500,
                                       required=False,
                                       widget=forms.Textarea,
                                       help_text='Enter up to 5 custom questions, each on a new line. Example:'
                                                 '"Mostly: 1.I am confident 2.I dont feel confident')

    class Meta:
        model = PsychoTest
        fields = ['name', 'image', 'description', 'threshold', 'result_above_threshold', 'result_below_threshold',
                  'questions']
        help_texts = {
            'name': 'Test name.',
            'image': 'Add image, if not default will be added.',
            'description': 'What is your test about.',
            'threshold': 'Set a integer number which will be the threshold for two results.',
            'result_above_threshold': 'Description of test result when score is above and equal threshold.',
            'result_below_threshold': 'Description of test result when score is below threshold.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['questions'].widget.attrs.update({'class': 'checkbox-list'})
        self.fields['questions'].label_from_instance = lambda obj: obj.question_content

    def save(self, commit=True):
        test = super().save(commit=False)
        if commit:
            test.save()
            self.save_m2m()
        custom_questions = self.cleaned_data.get('custom_questions')
        if custom_questions:
            custom_questions_list = custom_questions.split('\n')
            for custom_question_content in custom_questions_list:
                if custom_question_content:
                    question = Question.objects.create(question_content=custom_question_content)
                    test.questions.add(question)
        return test
