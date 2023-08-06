"""
This module provides the base class that is used to wrap the various DAG task methods. It
provides support for user-defined setup and cleanup, task monitoring using Elastic APM,
standardized logging and exception handling.
"""
import logging
from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from typing import Optional

import elasticapm


__all__ = ["TaskBase"]

logger = logging.getLogger(__name__)


class ApmTransaction:
    """
    Elastic APM transaction manager for a DAG Task.
        Without configuration it self disables
    """

    def __init__(self, transaction_name: str, apm_client_config: Optional[dict] = None) -> None:
        self.configured = bool(apm_client_config)
        if self.configured:
            self.transaction_name = transaction_name
            self.client = elasticapm.Client(apm_client_config)
            elasticapm.instrument()
            self.client.begin_transaction(self.transaction_name)

    @contextmanager
    def capture_span(self, name: str, *args, **kwargs):
        if not self.configured:
            try:
                yield
            finally:
                pass
        else:
            try:
                with elasticapm.capture_span(name, *args, **kwargs):
                    yield
            finally:
                pass

    def close(self):
        if not self.configured:
            return
        self.client.end_transaction(self.transaction_name)
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # note: exception not captured through apm due to potential size of local variables


class TaskBase(ABC):
    """
    Generic wrapper for the DAG tasks providing a standard interface and execution flow.
    Each DAG task must implement its own subclass of this abstract wrapper class.
    Intended instantiation is as a context manager
    >>> class RealTask(TaskBase):
    >>>     def run(self):
    >>>         pass
    >>>
    >>> with RealTask(1, "a", "b") as task:
    >>>     task()

    Task names in airflow are the same as the class name
    Additional methods can be added but will only be called if they are referenced via run,
      pre_run, post_run, or __exit__

    overriding methods other than run, pre_run, post_run, and in
      special cases __exit__ is discouraged as they are used internally to support the abstraction.
      e.g. __init__ is called by the core api without user involvement so adding parameters will not
      result in them being passed in as there is no client interface to __init__.

    To use the apm infrastructure in subclass code one would do the following:
    >>> def foo(self):
    >>>     with self.apm_step("do detailed work"):
    >>>         pass # do work
    """

    retries = 0
    retry_delay_seconds = 60

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
        apm_client_config: Optional[dict] = None,
    ):
        self.recipe_run_id = int(recipe_run_id)
        self.workflow_name = workflow_name
        self.workflow_version = workflow_version
        self.apm_client_configuration = apm_client_config
        self.task_name = self.__class__.__name__
        logger.info(f"Task {self.task_name} initialized")
        self.apm = ApmTransaction(
            transaction_name=self.task_name, apm_client_config=self.apm_client_configuration
        )
        self.apm_step = self.apm.capture_span  # abbreviated syntax for capture span context mgr

    def pre_run(self) -> None:
        """
        Method intended to be overridden that will execute prior to run() with Elastic APM span
          capturing
        """

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method that must be overridden to execute the desired DAG task.
        """

    def post_run(self) -> None:
        """
        Method intended to be overridden that will execute after run() with Elastic APM span
          capturing
        """

    def __call__(self) -> None:
        """
        The main executable function for the DAG task wrapper. Execution is instrumented with
        Application Performance Monitoring if configured. The standard execution sequence is:\n
        1 run
        2 record provenance

        Returns
        -------
        None
        """

        logger.info(f"Task {self.task_name} started")
        with self.apm_step("Pre Run"):
            self.pre_run()
        with self.apm_step("Run"):
            self.run()
        with self.apm_step("Post Run"):
            self.post_run()
        logger.info(f"Task {self.task_name} complete")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Method that can be overridden to execute teardown tasks after task execution regardless
          of task execution success.  Only override this method with tasks that need to happen
          regardless of tasks having an exception, ensure that no additional exception
          will be raised, and always call super().__exit__
        """
        self.apm.close()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"recipe_run_id={self.recipe_run_id}, "
            f"workflow_name={self.workflow_name}, "
            f"workflow_version={self.workflow_version}, "
            f"apm_client_config={self.apm_client_configuration}"
            f")"
        )

    def __str__(self):
        return repr(self)
