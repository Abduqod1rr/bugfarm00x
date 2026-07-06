import os
from django.db import migrations
from django.core.files import File


def update_seed_posts(apps, schema_editor):
    Poc = apps.get_model('main', 'Poc')
    titles = ['Welcome to PicPok!', 'Check this out', 'Hello World', 'PicPok rocks!']
    dino_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Google Dino Online.jpeg')

    for i, title in enumerate(titles, 1):
        poc = Poc.objects.filter(title=title).first()
        if poc:
            with open(dino_path, 'rb') as f:
                poc.content.save(f'seed_post_{i}.jpeg', File(f), save=True)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_poc_content_alter_profile_picture'),
    ]

    operations = [
        migrations.RunPython(update_seed_posts),
    ]
