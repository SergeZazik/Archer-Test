from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'archer_apps.accounts'

    def ready(self):
        import archer_apps.accounts.signals
