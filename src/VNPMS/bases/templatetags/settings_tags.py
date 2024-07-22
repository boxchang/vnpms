from django import template

from projects.models import Project, Project_setting

register = template.Library()

@register.simple_tag
def project_default(request):
    pk = ''
    settings = Project_setting.objects.filter(user=request.user)
    if request.user and Project.objects.all().count() > 0 and settings:
        pk = request.user.setting_user.first().default.pk
    return pk