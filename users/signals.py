# from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete,pre_delete
# from django.dispatch import receiver

# from django.contrib.auth.models import User,Group





# @receiver(post_save,sender=User)
# def assign_role(sender,instance,created,**kwargs):
#     if created:
#         user_group,created=Group.objects.get_or_create(name='Clents')
#         instance.groups.add(user_group)
#         instance.save()