# Magic module initialization
from magic.word import magic_transform, is_there_magic_word, magic_replace
from magic.script import process_magic_script, process_command

__all__ = [
    'magic_transform', 
    'is_there_magic_word', 
    'magic_replace',
    'process_magic_script',
    'process_command'
]