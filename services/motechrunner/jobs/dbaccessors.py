from jobs.filter_matching import filter_matches_message
from jobs.models import Job


def get_jobs_for_stream(stream):
    return Job.objects.raw("""
      SELECT * FROM jobs_job AS job INNER JOIN (
        SELECT job.uuid, MAX(job.rev) AS rev
        FROM jobs_job as job
        WHERE stream_id = %(stream_id)s
        GROUP BY job.uuid
      ) job_inner
      ON stream_id = %(stream_id)s AND job.rev = job_inner.rev AND job.uuid = job_inner.uuid
      ORDER BY job.modified
    """, {'stream_id': stream.id})


def get_jobs_matching_message(stream, message):
    jobs = get_jobs_for_stream(stream)
    return [job for job in jobs if filter_matches_message(job.filter, message)]
