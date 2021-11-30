import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
    '''
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently()는 
        pub_date가 미래인 질문에 대해 False를 반환합니다.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    '''
    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    주어진 'question_text'로 질문을 만들고 주어진 
    'days' 오프셋을 지금까지 게시했습니다
    (과거에 게시된 질문의 경우 음수, 
    아직 게시되지 않은 질문의 경우 양수).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        질문이 없으면 해당 메시지가 표시됩니다.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        과거에 pub_date가 있는 질문은 
        색인 페이지에 표시됩니다.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        '''
        미래의 pub_date가 
        있는 질문은 색인 페이지에 표시되지 않습니다.
        '''
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
    
    def test_future_question_and_past_question(self):
        '''
        과거 질문과 미래 질문이 모두 
        존재하더라도 과거 질문만 표시됩니다.
        '''
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        질문 색인 페이지에는 여러 질문이 표시될 수 있습니다.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        미래의 pub_date가 있는 질문의 세부 정보 보기는 
        404 not found를 반환합니다.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        과거에 pub_date가 있는 질문의 세부 정보 보기에는 
        질문의 텍스트가 표시됩니다.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    