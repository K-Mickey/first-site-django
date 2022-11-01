from django.db.models import Count
from django.core.cache import cache

from photo.models import *

menu = [
    {"title": "О сайте", 'url_name': 'about'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
 ]

class DataMixin:
    paginate_by = 10

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('photo'))
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if self.request.user.is_authenticated:
            user_menu.insert(0, {'title': 'Добавить пост', 'url_name': 'add_post'})

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
