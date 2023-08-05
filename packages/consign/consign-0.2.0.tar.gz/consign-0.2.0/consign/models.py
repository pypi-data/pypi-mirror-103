import os
import sys
import json
import errno
import tempfile

from os.path import isfile

from .exceptions import (
    InvalidDataType, InvalidPath, InvalidPermissions, InvalidCloudProvider,
    InvalidConnectionString, InvalidContainerName, InvalidBlobName,
    InvalidTableName, ConsignWarning)

# Sadly, Python fails to provide the following magic number for us.
# Windows-specific error code indicating an invalid path.
ERROR_INVALID_NAME = 123


class Consignment():
    '''A user-created :class:`Consignment <Consignment>` object.
    Used to prepare a :class:`PreparedConsignment <PreparedConsignment>`, which is sent to the server.
    '''

    def __init__(self,
        method=None, data=None, path=None, delimiter=None, overwrite=True,
        initialize=False, provider=None, connection_string=None,
        container_name=None):

        # Default empty dicts for optional dict params.
        default_delimiter = ',' if method == 'CSV' else None
        delimiter = default_delimiter if delimiter == None else delimiter

        self.method = method
        self.data = data
        self.path = path
        self.delimiter = delimiter
        self.overwrite = overwrite
        self.initialize = initialize
        self.provider = provider.strip().lower() if provider else None
        self.connection_string = connection_string
        self.container_name = container_name



class PreparedConsignment():
    '''The fully mutable :class:`PreparedConsign <PreparedConsign>` object,
    containing the exact bytes that will be sent to the server.
    Instances are generated from a :class:`Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.
    '''

    def __init__(self):
        pass


    def prepare(self,
        method=None, data=None, path=None, delimiter=None, overwrite=None,
        initialize=False, provider=None, connection_string=None,
        container_name=None):
        '''Prepares the entire consignment with the given parameters.'''

        self.prepare_method(method)
        self.prepare_data(data, delimiter)
        self.prepare_path(path, provider, initialize)
        self.prepare_file(path, overwrite)

        self.prepare_provider(provider)
        self.prepare_connection_string(provider, connection_string)
        self.prepare_container_name(provider, container_name)

        # Note that prepare_auth must be last to enable authentication schemes
        # such as OAuth to work on a fully prepared request.


    def prepare_provider(self, provider):
        '''
        Checks if given provider is listed and valid.
        '''
        listed_providers = ['azure']
        if provider and provider not in listed_providers:
            msg = '"{}" is not a valid cloud provider'.format(provider)
            raise InvalidCloudProvider(msg)
        self.provider = provider


    def prepare_connection_string(self, provider, connection_string):
        '''
        As required by Azure in their docs:
        https://docs.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string
        '''
        msg = None
        if connection_string and provider == 'azure':
            BASE_MESSAGE = 'In Azure Storage, '

            connection_dic = {
                item.split('=')[0]:item.split('=')[1] for item in connection_string.split(';')}
            protocol = connection_dic.get('DefaultEndpointsProtocol', None)
            account_name = connection_dic.get('AccountName', None)
            account_key = connection_dic.get('AccountKey', None)

            if not protocol:
                msg = 'the connection protocol, HTTPS or HTTP, must be indicated using "DefaultEndpointsProtocol".'
            elif not (protocol == 'http' or  protocol == 'https'):
                msg = 'the connection protocol must be HTTP or HTTPS, indicated in lowercase.'

            if not account_name:
                msg = 'your storage account name must be indicated using "AccountName".'
            
            if not account_key:
                msg = 'your storage account access key must be indicated using "AccountKey".'

        if msg: raise InvalidConnectionString(BASE_MESSAGE + msg)

        self.connection_string = connection_string


    def prepare_container_name(self, provider, container_name):
        '''
        As required by Azure in their docs:
        https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names
        '''
        msg = None
        if container_name and provider == 'azure':
            BASE_MESSAGE = 'In Azure Storage, '
            
            for character in container_name:
                if not (character.islower() or character.isdigit() or character == '-'):
                    msg = 'container names can only contain lowercase letters, numbers or dashes ("-").'
            
            if '--' in container_name:
                msg = 'consecutive dashes ("--") are not permitted in container names.'
            
            if len(container_name) < 3 or len(container_name) > 63:
                msg = 'container names must be from 3 through 63 characters long.'

        if msg: raise InvalidContainerName(BASE_MESSAGE + msg)

        self.container_name = container_name


    def prepare_method(self, method):
        '''Prepares the given Consignment method.'''
        self.method = method.upper()


    def prepare_data(self, data, delimiter):

        self.delimiter = delimiter

        if self.method == 'CSV':
            self.prepare_csv(data, delimiter)
        
        elif self.method == 'JSON':
            self.prepare_json(data)
        
        else: # @TODO: Add validations for binary files, blobs, etc.
            self.data = data


    def prepare_json(self, data):
        '''Verifies data is valid JSON.
        '''
        if not isinstance(data, (list, dict)) or not self.is_json_safe(data):
            raise InvalidDataType('Data is not a valid JSON object.')
        self.data = data


    def is_json_safe(self, data): 
        if data is None:
            return True 
        elif isinstance(data, (bool, int, float, str)): 
            return True 
        elif isinstance(data, (tuple, list)): 
            return all(self.is_json_safe(x) for x in data) 
        elif isinstance(data, dict):
            return all(isinstance(k, str) and self.is_json_safe(v) for k, v in data.items())
        return False 


    def prepare_csv(self, data, delimiter):
        '''
        Verifies data is tabular and free of delimiter characters.
        '''
        is_tabular = isinstance(data, list)
        if not is_tabular:
            raise InvalidDataType('Data is not tabular.')

        is_free = not(any(delimiter in column for row in data for column in row))
        if not is_free:
            raise ConsignWarning('Delimiter %s is used in data' % (delimiter))

        self.data = data
        self.delimiter = delimiter


    def prepare_path(self, path, provider, initialize):
        '''
        Verifies path existance, user permissions to write, and file extension
        matches the data format.
        '''
        if self.method in ['CSV', 'JSON', 'PDF', 'HTML', 'TXT']:
            self.prepare_file_path(path, initialize)
        elif self.method == 'BLOB':
            self.prepare_blob_name(path, provider)
        elif self.method == 'TABLE':
            self.prepare_table_name(path, provider)
        self.path = path


    def prepare_blob_name(self, path, provider):
        '''
        As required by Azure in their docs:
        https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#blob-names
        '''
        msg = None
        if provider == 'azure':
            
            BASE_MESSAGE = 'In Azure Storage, '

            if len(path) < 1 or len(path) > 1024:
                msg = 'blob names must be from 1 through 1024 characters long.'
            
            path_segments = path.split('/')
            if len(path_segments) > 254:
                msg = 'the number of path segments comprising the blob name cannot exceed 254.'

            for path_segment in path_segments:
                if path_segment.endswith('.'):
                    msg = "blob names' path segments should not end with a dot."

            if path.endswith('/'):
                msg = 'blob names should not end with a forward slash.'
        
        if msg: raise InvalidBlobName(BASE_MESSAGE + msg)


    def prepare_table_name(self, path, provider):
        '''
        '''
        msg = None
        if path and provider == 'azure':
            BASE_MESSAGE = 'In Azure Storage, '
            
            for character in path:
                if not (character.isalpha() or character.isdigit()):
                    msg = 'table names can only contain alphanumeric characters.'
            
            if path[0].isdigit():
                msg = 'table names may not begin with a numeric character.'
            
            if len(path) < 3 or len(path) > 63:
                msg = 'table names must be from 3 through 63 characters long.'

        if msg: raise InvalidTableName(BASE_MESSAGE + msg)


    def is_path_valid(self, path):
        '''
        `True` if the passed path is a valid path for the current OS;
        `False` otherwise.
        '''
        # If this path is either not a string or is but is empty, this path
        # is invalid.
        try:
            if not isinstance(path, str) or not path:
                raise InvalidPath('Path is not valid')

            # Strip this path's Windows-specific drive specifier (e.g., `C:\`)
            # if any. Since Windows prohibits path components from containing `:`
            # characters, failing to strip this `:`-suffixed prefix would
            # erroneously invalidate all valid absolute Windows paths.
            _, path = os.path.splitdrive(path)

            # Directory guaranteed to exist. If the current OS is Windows, this is
            # the drive to which Windows was installed (e.g., the '%HOMEDRIVE%'
            # environment variable); else, the typical root directory.
            root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                if sys.platform == 'win32' else os.path.sep
            assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

            # Append a path separator to this directory if needed.
            root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

            # Test whether each path component split from this path is valid or
            # not, ignoring non-existent and non-readable path components.
            for path_part in path.split(os.path.sep):
                try:
                    os.lstat(root_dirname + path_part)
                # If an OS-specific exception is raised, its error code
                # indicates whether this path is valid or not. Unless this
                # is the case, this exception implies an ignorable kernel or
                # filesystem complaint (e.g., path not found or inaccessible).
                #
                # Only the following exceptions indicate invalid paths:
                #
                # * Instances of the Windows-specific 'WindowsError' class
                #   defining the 'winerror' attribute whose value is
                #   'ERROR_INVALID_NAME'. Under Windows, 'winerror' is more
                #   fine-grained and hence useful than the generic 'errno'
                #   attribute. When a too-long path is passed, for example,
                #   'errno' is 'ENOENT' (i.e., no such file or directory) rather
                #   than 'ENAMETOOLONG' (i.e., file name too long).
                # * Instances of the cross-platform 'OSError' class defining the
                #   generic 'errno' attribute whose value is either:
                #   * Under most POSIX-compatible OSes, 'ENAMETOOLONG'.
                #   * Under some edge-case OSes (e.g., SunOS, *BSD), 'ERANGE'.
                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == ERROR_INVALID_NAME:
                            raise InvalidPath('Path is not valid')
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        raise InvalidPath('Path is not valid')
        except TypeError as exc:
            raise InvalidPath('Path is not valid')


    def is_path_creatable(self, path):
        '''
        Checks if the user has sufficient permissions to write in the given path.
        '''
        dirname = os.path.dirname(path) or os.getcwd()
        if not os.access(dirname, os.W_OK):
            raise InvalidPermissions('User is unauthorized to write in path')


    def is_path_extension_adecuate(self, path):
        '''
        '''
        given_method = self.method.lower()
        given_extension = path.split('.')[-1]
        if not given_extension == given_method:
            raise InvalidPath('Wrong file extension. Should be "%s" instead of "%s"' % (given_method, given_extension))
        return True


    def is_path_available(self, path):
        '''
        '''
        directory_path = "/".join(path.split("/")[:-1])
        if not os.path.exists(directory_path) and not self.initialize:
            raise InvalidPath('No such directory: {}'.format(directory_path))


    def prepare_file_path(self, path, initialize):
        '''
        Source: https://stackoverflow.com/a/34102855
        'True' if the passed path is a valid path for the current OS _and_
        either currently exists or is hypothetically creatable; 'False' otherwise.

        This function is guaranteed to _never_ raise exceptions.
        '''
        self.initialize = initialize
        self.is_path_available(path)
        self.is_path_valid(path) 
        # self.is_path_creatable(path) # @TODO: Fix, always raises error.

        if not self.method == 'IMG':
            self.is_path_extension_adecuate(path)


    def prepare_file(self, path, overwrite):
        '''
        If file is to be updated, it needs to exist.
        '''
        self.overwrite = overwrite
        if not self.overwrite and self.method in ['CSV', 'JSON']:
            if not isfile(path):
                raise InvalidPath('No such file: {}'.format(path))
