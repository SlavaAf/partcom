from django import template
from accounts.models import PostComment

register = template.Library()


@register.inclusion_tag('accounts/templatetags/comment_tree.html', takes_context=True)
def comment_tree(context, answer_to):
    children = PostComment.objects.filter(answer_to=answer_to)
    return {'answer_to': answer_to, 'children': children}
