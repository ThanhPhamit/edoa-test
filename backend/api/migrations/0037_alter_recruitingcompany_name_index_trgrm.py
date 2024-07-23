from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models

# api_recruitingcompany will be a large table (~5,000,000 rows) and needs to be support fast ILIKE queries.
# This migration adds a trigram index to the "name" column of api_recruitingcompany.

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_alter_proposal_summary')
    ]

    operations = [
        TrigramExtension(),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS api_recruitingcompany_name_trgm on api_recruitingcompany USING GIN (name gin_trgm_ops);"
        ),
    ]
