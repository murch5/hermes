import os
import magic
import mimetypes



def check_file_mime(path_in):

    #mime_type_libmagic = magic.from_file(path_in, mime=True)
    mime_type_mimetypes = mimetypes.guess_type(path_in)

    return mime_type_mimetypes[0]

def check_file_mime_from_buffer(path_in):
    print(path_in)
    return magic.from_buffer(path_in.read(), mime=True)

def get_name_from_path(path):

    _, tail = os.path.split(path)

    return tail

