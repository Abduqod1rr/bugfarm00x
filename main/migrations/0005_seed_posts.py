from django.db import migrations
from django.core.files.base import ContentFile


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

    for i, title in enumerate(seed_posts, 1):
        if not Poc.objects.filter(title=title, owner=demo_user).exists():
            poc = Poc(title=title, owner=demo_user)
            filename = f'seed_post_{i}.txt'
            poc.content.save(filename, ContentFile(f'Content for: {title}'), save=True)


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
