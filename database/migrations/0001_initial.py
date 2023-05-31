# Generated by Django 4.2.1 on 2023-05-10 18:34

import database.mixins.file_and_source_mixin
import django.contrib.postgres.fields
import django.contrib.postgres.fields.ranges
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of this Archive', max_length=200)),
                ('url', models.URLField(blank=True, help_text='The URL of the Archive', null=True)),
            ],
            options={
                'verbose_name_plural': 'Archives',
                'db_table': 'archive',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContributionMusicalWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('role', models.CharField(choices=[('COMPOSER', 'Composer'), ('ARRANGER', 'Arranger'), ('AUTHOR', 'Author of Text'), ('TRANSCRIBER', 'Transcriber'), ('IMPROVISER', 'Improviser'), ('PERFORMER', 'Performer')], default='COMPOSER', help_text='The role that this Person had in contributing. Can be one of: Composer, Arranger, Author of Text, Transcriber, Improviser, Performer', max_length=30)),
                ('certainty_of_attribution', models.BooleanField(blank=True, help_text='Whether it is certain if this Person made this contribution', null=True)),
                ('date_range_year_only', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='The year range of this contribution. If the year is known precisely, enter only one value. If not, enter a lower and upper bound', null=True)),
            ],
            options={
                'verbose_name': 'Contribution to Musical Work',
                'verbose_name_plural': 'Contributions to Musical Works',
                'db_table': 'contribution_musical_work',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EncodingWorkFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('encoder_names', models.CharField(blank=True, help_text='The names of the persons that encoded a file', max_length=512, null=True)),
                ('workflow_text', models.TextField(blank=True, help_text='A description of the workflow that was used to encode a Filein the database', null=True)),
                ('workflow_file', models.FileField(blank=True, help_text='A file that describes or defines the workflow that was used to encode a File in the database', max_length=255, null=True, upload_to='workflows/')),
                ('notes', models.TextField(blank=True, help_text='Any extra notes or remarks the user wishes to provide', null=True)),
            ],
            options={
                'verbose_name_plural': 'Encoding Workflows',
                'db_table': 'encoding_workflow',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('file_type', models.CharField(choices=[('sym', 'Symbolic Music'), ('txt', 'Text'), ('img', 'Image'), ('audio', 'Audio')], default='sym', help_text='The type of the file', max_length=10)),
                ('file_format', models.CharField(help_text='The format of the file', max_length=10)),
                ('version', models.CharField(blank=True, help_text='The version of the encoding schema i.e. MEI 2.0', max_length=20, null=True)),
                ('encoding_date', models.DateTimeField(blank=True, help_text='The date the File was encoded', null=True)),
                ('licensing_info', models.TextField(blank=True, help_text='Any licensing information related to this file', null=True)),
                ('extra_metadata', models.JSONField(blank=True, help_text='Any extra metadata associated with the File', null=True)),
                ('file', models.FileField(help_text='The actual file', max_length=255, upload_to='user_files/')),
                ('original_file_name', models.CharField(blank=True, help_text='The original name of the file when uploaded, to be filled automatically', max_length=255, null=True)),
                ('encoding_workflow', models.ForeignKey(blank=True, help_text='The Encoding Workflow of this File', null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.encodingworkflow')),
            ],
            options={
                'verbose_name_plural': 'Files',
                'db_table': 'files',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenreAsInStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of the GenreAsInStyle', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Genres as in Style',
                'db_table': 'genre_as_in_style',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenreAsInType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of the GenreAsInStyle', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Genres as in Type',
                'db_table': 'genre_as_in_type',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeographicArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of the Geographic Area', max_length=200)),
                ('authority_control_url', models.URLField(blank=True, help_text='An URI linking to an authority control description of this Geographic Area', null=True)),
                ('part_of', models.ForeignKey(blank=True, help_text='The "parent area" of this Geographic Area. Example: Montreal has as parent area Quebec', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_areas', to='database.geographicarea')),
            ],
            options={
                'verbose_name_plural': 'Geographic Areas',
                'db_table': 'geographic_area',
            },
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of the Instrument or Voice', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Instruments',
                'db_table': 'instrument',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of the Language', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Languages',
                'db_table': 'language',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MusicalWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('variant_titles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), help_text='All the titles commonly attributed to this musical work. Include the opus or catalogue number if there is one.', size=None)),
                ('sacred_or_secular', models.BooleanField(blank=True, default=None, help_text='Leave blank if not applicable.', null=True)),
                ('authority_control_url', models.URLField(blank=True, help_text='URI linking to an authority control description of this musical work.', null=True)),
                ('search_document', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Musical Works',
                'db_table': 'musical_work',
                'abstract': False,
            },
            bases=(database.mixins.file_and_source_mixin.FileAndSourceMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(blank=True, help_text='The name of this Part (e.g. Guitar, Violin II)', max_length=200, null=True)),
                ('musical_work', models.ForeignKey(blank=True, help_text='The MusicalWork to which this Part belongs', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='database.musicalwork')),
            ],
            options={
                'verbose_name_plural': 'Parts',
                'db_table': 'part',
                'abstract': False,
            },
            bases=(database.mixins.file_and_source_mixin.FileAndSourceMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('title', models.CharField(help_text='The title of this Section', max_length=200)),
                ('ordering', models.PositiveIntegerField(blank=True, help_text='A number representing the position of this Section within a Musical Work', null=True)),
                ('musical_work', models.ForeignKey(help_text='Reference to the MusicalWork of which this Section is part. A Section must reference a MusicalWork even if it has parent Sections', on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='database.musicalwork')),
                ('parent_section', models.ForeignKey(blank=True, help_text='Sections that contain his Section', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child_sections', to='database.section')),
                ('related_sections', models.ManyToManyField(blank=True, help_text='Sections that are related to this Section (i.e. derived from it, or the same music but used in a different MusicalWork)', to='database.section')),
            ],
            options={
                'verbose_name_plural': 'Sections',
                'db_table': 'section',
                'abstract': False,
            },
            bases=(database.mixins.file_and_source_mixin.FileAndSourceMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of the Software', max_length=100)),
                ('version', models.CharField(blank=True, default='', help_text='The version of the Software', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Software',
                'db_table': 'software',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('title', models.CharField(help_text='The title of this Source', max_length=200)),
                ('source_type', models.CharField(choices=[('MANUSCRIPT', 'Manuscript'), ('PRINT', 'Print'), ('DIGITAL', 'Digital')], default='PRINT', help_text='The type of this Source', max_length=30)),
                ('editorial_notes', models.TextField(blank=True, help_text='Any editorial notes the user deems necessary', null=True)),
                ('url', models.URLField(blank=True, help_text='An URL that identifies this Source', null=True)),
                ('date_range_year_only', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='The year range of this Source. If the year is known precisely, enter only one value. If not, enter a lower and upper bound', null=True)),
                ('in_archive', models.ForeignKey(blank=True, help_text='The Archive where this Source can be found', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sources', to='database.archive')),
                ('languages', models.ManyToManyField(blank=True, help_text='e.g., Latin, French, English', related_name='sources', to='database.language')),
                ('parent_source', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child_source', to='database.source')),
            ],
            options={
                'verbose_name_plural': 'Sources',
                'db_table': 'source',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeOfSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of this Type of Section', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Types of Section',
                'db_table': 'type_of_section',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ValidationWorkFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('validator_names', models.CharField(blank=True, help_text='The person(s) that validated a file', max_length=512, null=True)),
                ('notes', models.TextField(blank=True, help_text='Any extra notes or remarks the user wishes to provide', null=True)),
                ('workflow_text', models.TextField(blank=True, help_text='A description of the workflow that was used to validate a Filein the database', null=True)),
                ('workflow_file', models.FileField(blank=True, help_text='A file that describes or defines the workflow that was used to validate a File in the database', max_length=255, null=True, upload_to='workflows/')),
                ('validator_software', models.ForeignKey(blank=True, help_text='The Software that was used in this Validation Workflow', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validation_workflows', to='database.software')),
            ],
            options={
                'verbose_name_plural': 'Validation Workflows',
                'db_table': 'validation_workflow',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SourceInstantiation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('portion', models.CharField(blank=True, max_length=200, null=True)),
                ('parts', models.ManyToManyField(blank=True, help_text='The Part or Parts manifested in full by this Source Instantiation', related_name='source_instantiations', to='database.part')),
                ('sections', models.ManyToManyField(blank=True, help_text='The Section or Sections manifested in full by this Source Instantiation', related_name='source_instantiations', to='database.section')),
                ('source', models.ForeignKey(help_text='The source represented by the file linked to this source instantiation', on_delete=django.db.models.deletion.CASCADE, related_name='source_instantiations', to='database.source')),
                ('work', models.ForeignKey(blank=True, help_text='The Musical Work manifested in part or in full by this Source Instantiation', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_instantiations', to='database.musicalwork')),
            ],
            options={
                'verbose_name_plural': 'Source Instantiations',
                'db_table': 'source_instantiation',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='section',
            name='type_of_section',
            field=models.ForeignKey(blank=True, help_text='The type of this section, e.g. Aria, Minuet, Chorus, Bridge', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='database.typeofsection'),
        ),
        migrations.CreateModel(
            name='ResearchCorpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('title', models.CharField(help_text='The title of this Research Corpus', max_length=200)),
                ('doi_links', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True, help_text='An DOI linking to a research corpus saved in Zenodo ', null=True), blank=True, null=True, size=None)),
                ('files', models.ManyToManyField(help_text='The Symbolic Music Files that his Research Corpus contains', related_name='in_corpora', to='database.file')),
            ],
            options={
                'verbose_name_plural': 'Research Corpora',
                'db_table': 'research_corpus',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('given_name', models.CharField(help_text='The given name of this Person', max_length=100)),
                ('surname', models.CharField(blank=True, default='', help_text='The surname of this Person, eave blank if it is unknown', max_length=100)),
                ('birth_date_range_year_only', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='The birth year range of this person. If the year is known precisely, enter only one value. If not, enter a lower and upper bound', null=True)),
                ('death_date_range_year_only', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, help_text='The death year range of this person. If the year is known precisely, enter only one value. If not, enter a lower and upper bound', null=True)),
                ('authority_control_url', models.URLField(blank=True, help_text='An URI linking to an authority control description of this Person', null=True)),
                ('birth_location', models.ForeignKey(blank=True, help_text='The birth location of this Person. Choose the most specific possible.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='birth_location_of', to='database.geographicarea')),
                ('death_location', models.ForeignKey(blank=True, help_text='The death location of this Person. Choose the most specific possible.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='death_location_of', to='database.geographicarea')),
            ],
            options={
                'verbose_name_plural': 'Persons',
                'db_table': 'person',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='part',
            name='section',
            field=models.ForeignKey(blank=True, help_text='The Section to which this Part belongs', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='database.section'),
        ),
        migrations.AddField(
            model_name='part',
            name='written_for',
            field=models.ForeignKey(help_text='The Instrument or Voice for which this Part is written', on_delete=django.db.models.deletion.PROTECT, related_name='parts', to='database.instrument'),
        ),
        migrations.AddField(
            model_name='musicalwork',
            name='contributors',
            field=models.ManyToManyField(blank=True, help_text='The persons that contributed to the creation of this Musical Work', through='database.ContributionMusicalWork', to='database.person'),
        ),
        migrations.AddField(
            model_name='musicalwork',
            name='genres_as_in_style',
            field=models.ManyToManyField(help_text='e.g., classical, opera, folk', related_name='musical_works', to='database.genreasinstyle'),
        ),
        migrations.AddField(
            model_name='musicalwork',
            name='genres_as_in_type',
            field=models.ManyToManyField(help_text='e.g., sonata, motet, 12-bar blues', related_name='musical_works', to='database.genreasintype'),
        ),
        migrations.AddField(
            model_name='musicalwork',
            name='related_works',
            field=models.ManyToManyField(blank=True, help_text='MusicalWorks that are related to this MusicalWork, for instance, one is an arrangement of the other', to='database.musicalwork'),
        ),
        migrations.AddField(
            model_name='file',
            name='instantiates',
            field=models.ForeignKey(help_text='The SourceInstantiation manifested by this File', on_delete=django.db.models.deletion.CASCADE, related_name='files', to='database.sourceinstantiation'),
        ),
        migrations.AddField(
            model_name='file',
            name='validation_workflow',
            field=models.ForeignKey(blank=True, help_text='The Validation Workflow of this File', null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.validationworkflow'),
        ),
        migrations.CreateModel(
            name='FeatureType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('name', models.CharField(help_text='The name of the FeatureType', max_length=200)),
                ('code', models.CharField(help_text='The jSymbolic code of the FeatureType', max_length=5)),
                ('description', models.TextField(blank=True, help_text='A description of the FeatureType')),
                ('is_sequential', models.BooleanField(blank=True, help_text='whether a feature can be extracted from sequential windows of a data instance (e.g. individual measures, sections, etc.); a value of true means that it can, a value of false means that only one feature value may be extracted per instance (i.e. per symbolic feature file)', null=True)),
                ('dimensions', models.PositiveIntegerField(help_text='The number of dimensions of the FeatureType')),
                ('min_val', models.FloatField(blank=True, help_text='The minimum value of this FeatureType across all files that have this feature', null=True)),
                ('max_val', models.FloatField(blank=True, help_text='The maximum value of this FeatureType across all files that have this feature', null=True)),
                ('software', models.ForeignKey(default='', help_text='The software that extracts this feature type', on_delete=django.db.models.deletion.PROTECT, related_name='feature_types', to='database.software')),
            ],
            options={
                'verbose_name_plural': 'Features',
                'db_table': 'feature',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeatureFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('file_format', models.CharField(help_text='The format of the FeatureFile', max_length=255)),
                ('file', models.FileField(help_text='The actual feature file', max_length=500, upload_to='user_files/feature_files')),
                ('config_file', models.FileField(help_text='A file describing the configuration used to extract the features', max_length=255, upload_to='user_files/extracted_features')),
                ('feature_definition_file', models.FileField(help_text='A file that defines the features represented in the FeatureFile', max_length=255, upload_to='user_files/extracted_features')),
                ('extracted_with', models.ForeignKey(help_text='The Software used to extract these features', on_delete=django.db.models.deletion.PROTECT, related_name='feature_files', to='database.software')),
                ('features_from_file', models.ForeignKey(help_text='The File that the features were extracted from', on_delete=django.db.models.deletion.CASCADE, related_name='feature_files', to='database.file')),
            ],
            options={
                'verbose_name_plural': 'Feature Files',
                'db_table': 'feature_file',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExtractedFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('value', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), help_text='The value of the Extracted Feature. Encoded as an array but if the Extracted Feature is scalar it is an array of length = 1', size=None)),
                ('extracted_with', models.ForeignKey(help_text='The Software used to extract this Extracted Feature', on_delete=django.db.models.deletion.PROTECT, related_name='features', to='database.software')),
                ('feature_files', models.ManyToManyField(help_text='The Feature Files that contain this feature', related_name='features', to='database.featurefile')),
                ('feature_of', models.ForeignKey(help_text='The File from which the feature was extracted', on_delete=django.db.models.deletion.CASCADE, related_name='features', to='database.file')),
                ('instance_of_feature', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='instances', to='database.featuretype')),
            ],
            options={
                'verbose_name_plural': 'Extracted Features',
                'db_table': 'extracted_feature',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExperimentalStudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date this entry was created')),
                ('date_updated', models.DateTimeField(auto_now=True, help_text='The date this entry was updated')),
                ('title', models.CharField(help_text='The title of the Experimental Study', max_length=200)),
                ('link', models.URLField(blank=True, help_text='A link to a paper of the Experimental Study')),
                ('authors', models.CharField(blank=True, help_text='The authors of this Experimental Study', max_length=512, null=True)),
                ('research_corpus_used', models.ForeignKey(help_text='The Research Corpus upon which this Experimental Study is based', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='studies', to='database.researchcorpus')),
            ],
            options={
                'verbose_name_plural': 'Experimental Studies',
                'db_table': 'experimental_study',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='encodingworkflow',
            name='encoding_software',
            field=models.ForeignKey(blank=True, help_text='The Software that was used in this Encoding Workflow', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='encoding_workflows', to='database.software'),
        ),
        migrations.AddField(
            model_name='contributionmusicalwork',
            name='contributed_to_work',
            field=models.ForeignKey(help_text='The Musical Work that the Person contributed to', on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='database.musicalwork'),
        ),
        migrations.AddField(
            model_name='contributionmusicalwork',
            name='location',
            field=models.ForeignKey(blank=True, help_text='The location in which this contribution happened', null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.geographicarea'),
        ),
        migrations.AddField(
            model_name='contributionmusicalwork',
            name='person',
            field=models.ForeignKey(help_text='The Person that contributed to a Musical Work', on_delete=django.db.models.deletion.PROTECT, related_name='contributions_works', to='database.person'),
        ),
        migrations.AddConstraint(
            model_name='source',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('date_range_year_only__startswith__isnull', False), ('date_range_year_only__endswith__isnull', False)), ('date_range_year_only__isnull', True), _connector='OR'), name='source_date_range_bounds_not_null'),
        ),
        migrations.AddConstraint(
            model_name='person',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('birth_date_range_year_only__startswith__isnull', False), ('birth_date_range_year_only__endswith__isnull', False)), ('birth_date_range_year_only__isnull', True), _connector='OR'), name='person_birth_range_bounds_not_null'),
        ),
        migrations.AddConstraint(
            model_name='person',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('death_date_range_year_only__startswith__isnull', False), ('death_date_range_year_only__endswith__isnull', False)), ('death_date_range_year_only__isnull', True), _connector='OR'), name='person_death_range_bounds_not_null'),
        ),
        migrations.AddConstraint(
            model_name='person',
            constraint=models.CheckConstraint(check=models.Q(('birth_date_range_year_only__fully_lt', models.F('death_date_range_year_only'))), name='death_later_than_birth'),
        ),
        migrations.AddConstraint(
            model_name='part',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('section__isnull', True), ('musical_work__isnull', False)), models.Q(('section__isnull', False), ('musical_work__isnull', True)), _connector='OR'), name='work_xor_section'),
        ),
        migrations.AddIndex(
            model_name='musicalwork',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_document'], name='musical_wor_search__ac3bb3_gin'),
        ),
        migrations.AddConstraint(
            model_name='contributionmusicalwork',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('date_range_year_only__startswith__isnull', False), ('date_range_year_only__endswith__isnull', False)), ('date_range_year_only__isnull', True), _connector='OR'), name='contribution_date_range_bounds_not_null'),
        ),
    ]
