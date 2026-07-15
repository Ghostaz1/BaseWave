import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='owner',
            field=models.OneToOneField(
                limit_choices_to={'role': 'shop_owner'},
                on_delete=django.db.models.deletion.CASCADE,
                related_name='shop',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]