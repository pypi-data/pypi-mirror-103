"""
Tests for the TaskBase functionality
"""
import pytest

from dkist_processing_core.task import TaskBase


@pytest.mark.parametrize(
    "apm_client_config",
    [
        pytest.param(None, id="NoAPM"),
        pytest.param(
            {
                "SERVICE_NAME": "test_task",  # Name of dag
                "ENVIRONMENT": "test",
                "SERVER_URL": "http://not.gonna.work.doc/",
            },
            id="NoAPM",
        ),
    ],
)
def test_task_execution(task_subclass, apm_client_config):
    """
    Given: Task subclass and parametrized APM configurations
    When: calling the instance
    Then: the run method is executed
    """
    task = task_subclass(
        recipe_run_id=1, workflow_name="", workflow_version="", apm_client_config=apm_client_config
    )
    task()
    assert task.pre_run_was_called
    assert task.run_was_called
    assert task.post_run_was_called


@pytest.mark.parametrize(
    "apm_client_config",
    [
        pytest.param(None, id="NoAPM"),
        pytest.param(
            {
                "SERVICE_NAME": "test_task",  # Name of dag
                "ENVIRONMENT": "test",
                "SERVER_URL": "http://not.gonna.work.doc/",
            },
            id="NoAPM",
        ),
    ],
)
def test_task_run_failure(error_task_subclass, apm_client_config):
    """
    Given: Task subclass and parametrized APM configurations
    When: calling the instance
    Then: the run method is executed
    """
    task = error_task_subclass(
        recipe_run_id=1, workflow_name="", workflow_version="", apm_client_config=apm_client_config
    )
    with pytest.raises(RuntimeError):
        task()


def test_base_task_instantiation():
    """
    Given: Abstract Base Class for a Task
    When: Instantiating base class
    Then: Receive TypeError
    """
    with pytest.raises(TypeError):
        t = TaskBase(recipe_run_id=1, workflow_name="", workflow_version="")


def test_task_subclass_instantiation(task_subclass):
    """
    Given: Subclass that implements abstract base task method(s)
    When: Instantiating subclass
    Then: Instance and Class attributes are set
    """
    recipe_run_id = 1
    workflow_name = "r2"
    workflow_version = "d2"
    is_task_manual = True
    apm_client_configuration = {
        "SERVICE_NAME": "test_task",
        "ENVIRONMENT": "test",
        "SERVER_URL": "http://not.gonna.work.doc/",
    }
    task = task_subclass(
        recipe_run_id=recipe_run_id,
        workflow_name=workflow_name,
        workflow_version=workflow_version,
        apm_client_config=apm_client_configuration,
        is_task_manual=is_task_manual,
    )
    # class vars
    assert task.retries == task_subclass.retries
    # instance vars
    assert task.recipe_run_id == recipe_run_id
    assert task.workflow_name == workflow_name
    assert task.workflow_version == workflow_version
    assert task.apm_client_configuration == apm_client_configuration
    assert task.is_task_manual == is_task_manual
    # calculated instance vars
    assert task.task_name == task_subclass.__name__


def test_repr_str(task_instance):
    """
    Given:  An instance of a task
    When: accessing the string or repr
    Then: Receive a value
    """
    assert str(task_instance)
    assert repr(task_instance)
