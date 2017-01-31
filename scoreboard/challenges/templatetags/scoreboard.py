import string

from django import template


register = template.Library()

@register.filter(name='ctf_describe')
def ctf_describe(challenge, request):
    address = request.get_host()
    host, _ = address.split(':', 1)
    static_path = '/static/{}/'.format(challenge.name)
    tmpl = string.Template(challenge.description)
    return tmpl.safe_substitute(PUBLIC_HOST=host,
                                PUBLIC_PORT=challenge.port,
                                STATIC_PATH=static_path)

