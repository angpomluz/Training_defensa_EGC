# Create your tests here.
import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from base import mods
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from base.tests import BaseTestCase
from voting.models import Voting, Question, QuestionOption
from visualizer.utils import readCSV
from visualizer.views import get_votes_by_age,calculate_age
import datetime

# Create your tests here.

class VisualizerTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='test voting', question=q)
        v.postproc=postprocs
        v.start_date=timezone.now()
        v.end_date=timezone.now()
        v.tally=5
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    #Voting without starting date
    def create_voting1(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='voting without starting date', question=q)
        v.postproc=postprocs
        v.tally=5
        v.save()
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    #Voting without ending date
    def create_voting2(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='voting without ending date', question=q)
        v.postproc=postprocs
        v.start_date=timezone.now()
        v.tally=5
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    #Voting without tally
    def create_voting3(self):
        q = Question(desc='test question')
        q.save()
        postprocs=[]
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
            postOpt={'votes':0,'number':i,'option':'option {}'.format(i+1),'postproc':0}
            postprocs.append(postOpt)
        v = Voting(name='test voting', question=q)
        v.postproc=postprocs
        v.start_date=timezone.now()
        v.end_date=timezone.now()
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def test_readCSV_positive(self):
        
        fpath="visualizer/resources/EGCusers.csv"
        read_users = readCSV(fpath)
        
        self.assertTrue(len(read_users) == 200)
        
    def test_readCSV_bad_path_negative(self):
        
        fpath="visualizer/resources/fakefile.csv"
        ex_catch = False
        try:
            readCSV(fpath)
        
        except(FileNotFoundError, IOError):
            ex_catch = True
            
        self.assertTrue(ex_catch)
            
    def test_get_votes_by_age_positive(self):
        
        read_users = readCSV("visualizer/resources/EGCusers.csv")
        
        age_range = [18,25,35,55,65]
        birthdates = [user['birthdate'] for user in read_users]
        votes_by_age = get_votes_by_age(age_range,birthdates)
        
        self.assertTrue(votes_by_age[18] > 0)
        
    def test_calculate_age_positive(self):
        
        born = "15/11/2000"
        age = calculate_age(born,True)
        
        self.assertTrue(age == 20)
        
    def test_calculate_age_bad_format_negative(self):
        
        err_triggered = False
        try:
            born = "2000/15/11"
            calculate_age(born,True)
            
        except(ValueError):
            err_triggered=True
        
        self.assertTrue(err_triggered)
        
        
        
        
        