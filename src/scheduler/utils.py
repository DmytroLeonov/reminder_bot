from src.scheduler import scheduler


def get_jobs(chat_id: int) -> list:
    return [job for job in scheduler.get_jobs() if job.kwargs["chat_id"] == chat_id]
