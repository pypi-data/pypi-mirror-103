import datetime
import typing

from lime_etl import domain

__all__ = ("DeleteOldLogs",)


class DeleteOldLogs(domain.JobSpec[domain.admin_unit_of_work.AdminUnitOfWork]):
    def __init__(
        self,
        days_logs_to_keep: domain.DaysToKeep = domain.DaysToKeep(3),
        min_seconds_between_runs: domain.MinSecondsBetweenRefreshes = domain.MinSecondsBetweenRefreshes(0),
    ):
        self._days_logs_to_keep = days_logs_to_keep
        self._min_seconds_between_runs = min_seconds_between_runs

    @property
    def job_name(self) -> domain.JobName:
        return domain.JobName("delete_old_logs")

    @property
    def min_seconds_between_refreshes(self) -> domain.MinSecondsBetweenRefreshes:
        return self._min_seconds_between_runs

    def run(
        self,
        admin_uow: domain.AdminUnitOfWork,
        batch_uow: domain.AdminUnitOfWork,
        logger: domain.JobLogger,
    ) -> domain.JobStatus:
        with batch_uow:
            batch_uow.batch_log_repo.delete_old_entries(days_to_keep=self._days_logs_to_keep)
            logger.log_info(
                f"Deleted batch log entries older than {self._days_logs_to_keep.value} days old."
            )

            batch_uow.job_log_repo.delete_old_entries(days_to_keep=self._days_logs_to_keep)
            logger.log_info(
                f"Deleted job log entries older than {self._days_logs_to_keep.value} days old."
            )

            batch_uow.batch_repo.delete_old_entries(self._days_logs_to_keep)
            logger.log_info(
                f"Deleted batch results older than {self._days_logs_to_keep.value} days old."
            )
            batch_uow.save()

        return domain.JobStatus.success()

    def test(
        self,
        admin_uow: domain.AdminUnitOfWork,
        batch_uow: domain.AdminUnitOfWork,
        logger: domain.JobLogger,
    ) -> typing.List[domain.SimpleJobTestResult]:
        with batch_uow:
            now = batch_uow.ts_adapter.now().value
            cutoff_date = datetime.datetime.combine(
                (now - datetime.timedelta(days=self._days_logs_to_keep.value)).date(),
                datetime.datetime.min.time(),
            )
            earliest_ts = batch_uow.batch_log_repo.get_earliest_timestamp()

        if earliest_ts and earliest_ts < cutoff_date:
            return [
                domain.SimpleJobTestResult(
                    test_name=domain.TestName("No log entries more than 3 days old"),
                    test_success_or_failure=domain.Result.failure(
                        f"The earliest batch log entry is from "
                        f"{earliest_ts.strftime('%Y-%m-%d %H:%M:%S')}"
                    ),
                )
            ]
        else:
            return [
                domain.SimpleJobTestResult(
                    test_name=domain.TestName("No log entries more than 3 days old"),
                    test_success_or_failure=domain.Result.success(),
                )
            ]
