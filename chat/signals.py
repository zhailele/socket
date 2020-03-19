from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from .views import Test_demo
from django.db.models.signals import post_save
from .models import User


@receiver(post_save,sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
# def create_user(sender, instance=None, updated=False, **kwargs):
    if created:
        print("*" * 50)
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        obj = User.objects.filter(id=3).first()
        name = obj.name

        obj2 = User.objects.filter(id=4).first()
        name2 = obj2.name

        # def send_channel_msg(channel_name,msg):
        #     async_to_sync(channel_layer.group_send)(channel_name,
        #                                         {"type": "system_message", "message": msg})
        def send_msg(channel_name,msg):
            async_to_sync(channel_layer.send)(channel_name,
                                                    {"type": "system_message", "message": msg})

        print("send------>group_send",name)
        print("send------>send",name2)

        # send_channel_msg(name,"充值成功!")

        send_msg(name2,"哈哈哈!")
    else:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        obj = User.objects.filter(id=3).first()
        name = obj.name

        obj2 = User.objects.filter(id=4).first()
        name2 = obj2.name

        def send_msg(channel_name, msg):
            async_to_sync(channel_layer.send)(channel_name,
                                              {"type": "system_message", "message": msg})


        print("send------>send", name2)
        send_msg(name2,"数据更新")





