from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator

supported_domains = {
    'twitter': 'https://twitter.com/',
    'instagram': 'https://www.instagram.com/',
    'telegram': 'https://t.me/',
    'tiktok': 'https://www.tiktok.com/@',
    'facebook': 'https://www.facebook.com/',
    'vk': 'https://vk.com/',
}


def process_link(input='', type=''):
    '''Если известный тип и это не ссылка,
    генерируем ссылку. Если уже ссылка,
    возвращаем ссылку. Если  неизвестный
    тип и не ссылка, то ничего не возвращаем.'''
    try:
        validator = URLValidator()
        validator(input)
        return input
    except ValidationError:
        if type == 'phone':
            return input
        elif type == 'email':
            try:
                e_validator = EmailValidator()
                e_validator(input)
                return input
            except ValidationError:
                return ''
        elif type not in supported_domains:
            return ''
        else:
            link = supported_domains[type] + input
        return link
