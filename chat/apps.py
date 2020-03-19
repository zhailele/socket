from django.apps import AppConfig


class ChatConfig(AppConfig):
    name = 'chat'
    verbose_name = "用户管理"

    def ready(self):
        import chat.signals
