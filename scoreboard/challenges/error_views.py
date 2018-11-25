from django.shortcuts import render_to_response


def handler400(request, template_name="400.html"):
    response = render_to_response(template_name)
    response.status_code = 400
    return response


def handler404(request, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="500.html"):
    response = render_to_response(template_name)
    response.status_code = 500
    return response

