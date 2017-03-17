import uuid
from django.test import TestCase
from jobs.dbaccessors import get_jobs_for_stream, get_jobs_matching_message
from jobs.models import Job
from streams.models import Stream


class DBAccessorsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stream = Stream(name='teststream')
        cls.stream.save()
        job_1_id = uuid.uuid4()
        job_2_id = uuid.uuid4()
        job_3_id = uuid.uuid4()
        cls.job_1_rev_1 = Job(stream=cls.stream, uuid=job_1_id, rev=1, filter={'type': 'Character'})
        cls.job_1_rev_2 = Job(stream=cls.stream, uuid=job_1_id, rev=2, filter={'type': 'Character'})
        cls.job_1_rev_3 = Job(stream=cls.stream, uuid=job_1_id, rev=3, filter={'type': 'Character'})
        cls.job_2_rev_1 = Job(stream=cls.stream, uuid=job_2_id, rev=1, filter={'type': 'setting'})
        cls.job_2_rev_2 = Job(stream=cls.stream, uuid=job_2_id, rev=2, filter={'type': 'Setting'})
        cls.job_3_rev_1 = Job(stream=cls.stream, uuid=job_3_id, rev=1, filter={'type': 'Plot'})
        cls.jobs = [
            cls.job_1_rev_1, cls.job_1_rev_2, cls.job_1_rev_3,
            cls.job_2_rev_1, cls.job_2_rev_2,
            cls.job_3_rev_1
        ]
        for job in cls.jobs:
            job.save()

    def test_get_jobs_for_stream(self):
        self.assertEqual(
            {(job.uuid, job.rev) for job in get_jobs_for_stream(self.stream)},
            {(job.uuid, job.rev) for job in [self.job_1_rev_3, self.job_2_rev_2,
                                             self.job_3_rev_1]}
        )

    def test_get_jobs_matching_message__matching(self):
        self.assertEqual(
            {(job.uuid, job.rev) for job in get_jobs_matching_message(
                self.stream, {'type': 'Character'})},
            {(job.uuid, job.rev) for job in [self.job_1_rev_3]}
        )

    def test_get_jobs_matching_message__no_match(self):
        self.assertEqual(
            {(job.uuid, job.rev) for job in get_jobs_matching_message(
                self.stream, {'true': 'blue'})},
            set()
        )

    @classmethod
    def tearDownClass(cls):
        for job in cls.jobs:
            job.delete()
        cls.stream.delete()
