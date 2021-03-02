from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

supported_domains = {
    'twitter': 'https://twitter.com/',
    'instagram': 'https://www.instagram.com/',
    'telegram': 'https://t.me/',
    'tiktok': 'https://www.tiktok.com/@',
    'facebook': 'https://www.facebook.com/',
    'vk': 'https://vk.com/',
}


def generate_link(nick='', type=''):
    '''Если известный тип и это не ссылка,
    генерируем ссылку. Если уже ссылка,
    возвращаем ссылку. Если  неизвестный
    тип и не ссылка, то ничего не возвращаем.'''
    try:
        validator = URLValidator()
        validator(nick)
        return nick
    except ValidationError:
        if type not in supported_domains:
            return ''
        else:
            link = supported_domains[type] + nick
        return link
