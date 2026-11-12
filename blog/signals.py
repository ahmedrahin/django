from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Post


# 1. Triggered ONLY when a blog post is CREATED
@receiver(post_save, sender=Post)
def post_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"\n================ [SIGNAL: CREATE] ================")
        print(f"🎉 NEW BLOG CREATED: '{instance.title}' (ID: {instance.id})")
        print(f"Category: {instance.category.name if instance.category else 'No Category'}")
        print(f"=================================================\n")


# 2. Triggered ONLY when a blog post is UPDATED (EDIT)
@receiver(post_save, sender=Post)
def post_updated_signal(sender, instance, created, **kwargs):
    if not created: 
        print(f"\n================ [SIGNAL: UPDATE / EDIT] ================")
        print(f"✏️ BLOG POST UPDATED: '{instance.title}' (ID: {instance.id})")
        print(f"Category: {instance.category.name if instance.category else 'No Category'}")
        print(f"========================================================\n")


# 3. [ADVANCED] pre_save:
@receiver(pre_save, sender=Post)
def post_pre_update_signal(sender, instance, **kwargs):
    if instance.pk:  # instance.pk থাকা মানে অবজেক্টটি আগে থেকেই ডেটাবেজে আছে (Update হচ্ছে)
        try:
            old_post = Post.objects.get(pk=instance.pk)
            if old_post.title != instance.title:
                print(f"🔄 Title changed from '{old_post.title}' -> to '{instance.title}'")
            
            # নতুন থাম্বনেইল দিলে পুরনো থাম্বনেইল স্বয়ংক্রিয়ভাবে মুছে ফেলা
            if old_post.thumb and old_post.thumb != instance.thumb:
                old_post.thumb.delete(save=False)
                print(f"📁 Old thumbnail auto-deleted via signal!")
        except Post.DoesNotExist:
            pass


# 4. Triggered when a blog post is DELETED
@receiver(post_delete, sender=Post)
def post_deleted_signal(sender, instance, **kwargs):
    print(f"\n=============== [SIGNAL: DELETE] ===============")
    print(f"🗑️ BLOG POST DELETED: '{instance.title}' (ID: {instance.id})")
    if instance.thumb:
        instance.thumb.delete(save=False)
        print(f"📁 Associated thumbnail file removed from storage.")
    print(f"================================================\n")
