from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def user_applied(context, position):
    for applicant in position.position_applicants.all():
        if applicant.user_profile == context['user']:
            return True
        return False
