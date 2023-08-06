NB_TYPE = '.ipynb'
UNTITLED_FILE = 'Untitled'
FOLDER_SEPERATOR = '/'
UNTITLED_NB = 'Untitled'
UNTITLED_FOLDER = 'Untitled Folder'
CHECKPOINT_NAME = '.checkpoints'
READ_HELPERS = {
('directory', 'json'): _get_folder,
('notebook', 'json'): _get_notebook,
('file', 'text'): _get_text_file,
('file', 'base64'): _get_base64_file
}

PUT_HELPERS = {
   ('file', 'base64'):  _save_base64_file,
    ('notebook', 'json'): _save_notebook,
    ('directory', 'json'): _save_folder,
    ('file', 'text'): _save_text_file
}

