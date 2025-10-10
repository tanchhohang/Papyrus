from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book
from django.core.cache import cache


@receiver([post_save,post_delete],sender=Book)
def invalidate_product_cache(sender,instance, **kwargs):
    print("Clearing book cache")

    if hasattr(cache, 'delete_pattern'):
        cache.delete_pattern('*book_list*')