nav = [
    {"title": "Главная", "url": "root"},
    {"title": "Самое свежее", "url": "root"},
    {"title": "Статьи", "url": "root"},
    {"title": "Категории", "url": "root"},
]

# class DataMixin:
#     page_title = None
#     cat_selected = None
#     paginate_by = 5
#     extra_context = {}
#
#     def __init__(self):
#         if self.page_title:
#             self.extra_context["title"] = self.page_title
#
#         if self.cat_selected is not None:
#             self.extra_context["cat_selected"] = self.cat_selected
#
#     def get_mixin_context(self, context, **kwargs):
#         context["cat_selected"] = None
#         context.update(kwargs)
#         return context