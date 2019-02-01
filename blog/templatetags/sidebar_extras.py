from django import template

register = template.Library()


@register.simple_tag
def get_another_page(paginator, page_num, shift):
    print(paginator, page_num, shift)
    return paginator.page(int(page_num) + int(shift))
