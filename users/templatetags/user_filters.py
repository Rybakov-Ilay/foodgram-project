from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(value, author):
    return author.favorites.filter(recipe=value, author=author).exists()


@register.filter
def is_purchase(value, author):
    return author.purchases.filter(recipe=value, author=author).exists()


@register.filter
def is_subscribe(value, author):
    return author.follower.filter(author=value).exists()


@register.filter
def check_tag(recipe):
    return list(recipe.tags.values_list('name', flat=True))


@register.filter
def get_tags(request):
    return request.getlist("tags")


@register.filter
def rebuild_tag_link(request, tag):
    request_copy = request.GET.copy()
    tags = request_copy.getlist("tags")
    if tag in tags:
        tags.remove(tag)
        request_copy.setlist("tags", tags)
    else:
        request_copy.appendlist("tags", tag)
    return request_copy.urlencode()


@register.filter
def url_with_get(request, page):
    query = request.GET.copy()
    query["page"] = page
    return query.urlencode()
