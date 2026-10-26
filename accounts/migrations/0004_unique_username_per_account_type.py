from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_username_not_unique'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='account',
            constraint=models.UniqueConstraint(
                fields=('username', 'account_type'),
                name='unique_username_per_account_type',
            ),
        ),
    ]
