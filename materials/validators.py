from rest_framework.serializers import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_link = dict(value).get(self.field)
        if tmp_link is not None:
            if 'youtube.com' in tmp_link:
                return True
            else:
                raise ValidationError('Такую ссылку нельзя использовать')