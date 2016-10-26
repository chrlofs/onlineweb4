from django.apps import AppConfig


class RutinatorConfig(AppConfig):
    name = 'apps.rutinator'
    verbose_name = 'Rutinator'

    def ready(self):
        super().ready()
        import apps.rutinator.signals  # flake8: noqa
