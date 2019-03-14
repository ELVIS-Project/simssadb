from database.models.symbolic_music_file import SymbolicMusicFile
from django.db.models.signals import post_save
from django.dispatch import receiver
import feature_extraction.feature_extraction
import os


@receiver(post_save, sender=SymbolicMusicFile)
def run_jsymbolic(sender, instance, **kwargs):
    path = os.path.join(os.getcwd() + '/media/', instance.file.name)
    print(path)
    print(os.path.exists(path))
    feature_extraction.feature_extraction.driver(path)
