from django import template

from problems.models import Problem_reply, Problem

register = template.Library()

@register.simple_tag
def get_problem_reply_num(problem_no):
    return Problem_reply.objects.filter(problem_no=Problem.objects.filter(problem_no=problem_no)).count()


@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except AttributeError:
        return None