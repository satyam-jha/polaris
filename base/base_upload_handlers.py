from django.utils import timezone


def get_extension(filename):
    return f".{filename.split('.')[-1]}"


def get_random_name(filename):
    split_filename = filename.split('.')
    no_ext_filename = ''.join([x for x in split_filename[:len(split_filename) - 1]][:50])
    return f'{no_ext_filename}-{int(timezone.now().timestamp() * 1000)}{get_extension(filename)}'


def handle_menu_file(instance, filename):
    new_filename = f'menu/{instance.user_id.hex}/{get_random_name(filename)}'
    return new_filename
