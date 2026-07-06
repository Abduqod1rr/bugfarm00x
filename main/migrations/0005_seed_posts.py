import os
from django.db import migrations
from django.core.files import File


def create_seed_posts(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Poc = apps.get_model('main', 'Poc')

    if not User.objects.filter(username='demo').exists():
        demo_user = User.objects.create_user(
            username='demo',
            password='demo1234',
        )
    else:
        demo_user = User.objects.get(username='demo')

    seed_posts = [
        'Welcome to PicPok!',
        'Check this out',
        'Hello World',
        'PicPok rocks!',
    ]

    dino_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Google Dino Online.jpeg')

    for i, title in enumerate(seed_posts, 1):
        if not Poc.objects.filter(title=title, owner=demo_user).exists():
            poc = Poc(title=title, owner=demo_user)
            with open(dino_path, 'rb') as f:
                poc.content.save(f'seed_post_{i}.jpeg', File(f), save=True)


def remove_seed_posts(apps, schema_editor):
    Poc = apps.get_model('main', 'Poc')
    Poc.objects.filter(title__in=[
        'Welcome to PicPok!', 'Check this out',
        'Hello World', 'PicPok rocks!',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_profile_picture'),
    ]

    operations = [
        migrations.RunPython(create_seed_posts, remove_seed_posts),
    ]
