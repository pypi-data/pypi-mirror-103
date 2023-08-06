"""Main bundle functionalities. Config, container and boot process"""
from pydantic import BaseModel
from dependency_injector import containers, providers
from applauncher.applauncher import Configuration
from kombu import Queue
from celery import Celery, signals
from typing import List
from multiprocessing import cpu_count
import logging


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    # Do not let celery configure loggers
    return True


class CeleryConfig(BaseModel):
    """More information about config here https://docs.celeryproject.org/en/latest/userguide/configuration.html"""
    name: str = 'celery'
    worker: bool = True
    # Arguments
    quiet: bool = True
    without_gossip: bool = True
    without_mingle: bool = True
    pool: str = 'prefork'
    # Parameters
    broker_url: str = 'pyamqp://guest@localhost//'
    task_queues: List[str] = ['default']
    result_backend: str = None
    task_serializer: str = 'json'
    accept_content: List[str] = ['json']
    result_serializer: str = 'json'
    result_expires: int = 3600  # 1 hour
    timezone: str = 'Europe/Madrid'
    worker_concurrency: int = cpu_count() * 2
    worker_max_tasks_per_child: int = None
    broker_pool_limit: int = None
    broker_heartbeat: int = 0  # Disabled, put some greater value if you network is not good
    broker_connection_timeout: int = 30
    event_queue_expires: int = None
    worker_prefetch_multiplier: int = 1  # Increase it in case you have a lot of fast tasks
    task_track_started: bool = True
    enable_utc: bool = True
    task_acks_late: bool = True
    worker_send_task_events: bool = True
    task_send_sent_event: bool = True
    include: List[str] = []


def create_client(config: CeleryConfig):
    """Split bundle config from celery parameters and arguments"""
    app = Celery(config.name)
    celery_config = config.dict()
    del celery_config['name']
    del celery_config['worker']
    del celery_config['quiet']
    del celery_config['without_gossip']
    del celery_config['without_mingle']
    celery_config['broker_heartbeat'] = None if celery_config['broker_heartbeat'] <= 0 else celery_config[
        'broker_hearhbeat']

    if celery_config['task_queues'] is not None:
        celery_config['task_queues'] = (Queue(task_name) for task_name in celery_config['task_queues'])

    app.conf.update(**{k: v for k, v in celery_config.items() if v is not None})
    return app


class CeleryContainer(containers.DeclarativeContainer):
    """Celery injectect values. You can crate a new application or reuse one"""
    config = providers.Dependency(instance_of=CeleryConfig)
    configuration = Configuration()
    celery = providers.Callable(
        create_client,
        config=configuration.provided.celery
    )
    app = providers.Singleton(celery)


class CeleryBundle:
    """The celery bundle. It loads the config, container and provides the worker start method"""
    def __init__(self):
        """We only use config and injections bindings"""
        self.config_mapping = {
            'celery': CeleryConfig
        }

        self.injection_bindings = {
            'celery': CeleryContainer
        }

    @staticmethod
    def start():
        """Parse the config and run the celery worker with the provided arguments"""
        config = CeleryContainer.configuration()
        if config.celery.worker:
            celery_config = config.celery  # type: CeleryConfig
            app = CeleryContainer.app()  # type: Celery
            params = []
            # Options
            if celery_config.quiet:
                params.append("--quiet")

            # Command
            params.append("worker")

            # Args
            if celery_config.without_gossip:
                params.append("--without-gossip")

            if celery_config.broker_heartbeat == 0:
                params.append("--without-heartbeat")

            if celery_config.without_mingle:
                params.append("--without-mingle")

            if celery_config.worker_send_task_events:
                params.append("-E")

            params.append("--pool")
            params.append(config.celery.pool)
            logging.getLogger("celery").info("Params: %s", " ".join(params))
            logging.getLogger("celery").info("Tasks: [[cyan]%s[/]]", ", ".join(app.conf["include"]))
            app.start(params)
