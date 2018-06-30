from django import template
from django.utils.safestring import mark_safe
from menu.models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    nodes = Menu.objects.get(name=menu_name).nodes
    an = context.request.path[1:]

    def tag(tag, text, ref='', id=''):
        """
            Обрамляет строку тэгом
        """
        if id and ref:
            return '<{0} href="{2}" id="{3}">{1}</{0}>'.format(tag, text, ref, id)
        if ref:
            return '<{0} href="{2}">{1}</{0}>'.format(tag, text, ref)
        elif id:
            return '<{0} id="{2}">{1}</{0}>'.format(tag, text, id)
        else:
            return '<{0}>{1}</{0}>'.format(tag, text)

    def flat(x):
        """
            Переводит вложенный словарь или список в плоский.
        """
        res = []
        if type(x) in (list, tuple):
            for i in x:
                res.extend(flat(i))
        elif isinstance(x, dict):
            for item in x.items():
                res.extend(flat(item))
        else:
            res.append(x)
        return res

    def draw_node(node, an):
        if an == node:
            return tag('li', tag('a', node, ref=node, id='active'))
        else:
            return tag('li', tag('a', node, ref=node))

    def draw_list(nodes, an):
        return ''.join(draw(node, an) for node in nodes)

    def draw_dict(nodes, an):
        res = ''
        for k, v in nodes.items():
            res += draw_node(k, an)
            if an == k:
                res += tag('ul', draw(v))
            elif an in flat(v):
                res += tag('ul', draw(v, an))
        return res

    def draw(nodes, an=''):
        if type(nodes) in (list, tuple):
            return draw_list(nodes, an)
        elif isinstance(nodes, dict):
            return draw_dict(nodes, an)
        else:
            return draw_node(nodes, an)

    return mark_safe(tag('ul', draw(nodes, an)))
