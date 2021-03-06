############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

import json as _json

import requests as _requests
import random as _random
import base64 as _base64

try:
    from urllib.parse import urlparse as _urlparse  # py3
except ImportError:
    from urlparse import urlparse as _urlparse  # py2

_CT = 'content-type'
_AJ = 'application/json'
_URL_SCHEME = frozenset(['http', 'https'])


def _get_token(user_id, password,
               auth_svc='https://nexus.api.globusonline.org/goauth/token?' +
                        'grant_type=client_credentials'):
    # This is bandaid helper function until we get a full
    # KBase python auth client released
    auth = _base64.b64encode((user_id + ':' + password).encode('utf-8'))
    headers = {'Authorization': 'Basic ' + auth.decode('utf-8')}
    ret = _requests.get(auth_svc, headers=headers, allow_redirects=True)
    status = ret.status_code
    if status >= 200 and status <= 299:
        tok = _json.loads(ret.text)
    elif status == 403:
        raise Exception('Authentication failed: Bad user_id/password ' +
                        'combination for user %s' % (user_id))
    else:
        raise Exception(ret.text)
    return tok['access_token']


class ServerError(Exception):

    def __init__(self, name, code, message, data=None, error=None):
        self.name = name
        self.code = code
        self.message = '' if message is None else message
        self.data = data or error or ''
        # data = JSON RPC 2.0, error = 1.1

    def __str__(self):
        return self.name + ': ' + str(self.code) + '. ' + self.message + \
            '\n' + self.data


class _JSONObjectEncoder(_json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, frozenset):
            return list(obj)
        return _json.JSONEncoder.default(self, obj)


class Workspace(object):

    def __init__(self, url=None, timeout=30 * 60, user_id=None,
                 password=None, token=None,
                 trust_all_ssl_certificates=False):
        if url is None:
            url = 'https://kbase.us/services/ws/'
        scheme, _, _, _, _, _ = _urlparse(url)
        if scheme not in _URL_SCHEME:
            raise ValueError(url + " isn't a valid http url")
        self.url = url
        self.timeout = int(timeout)
        self._headers = dict()
        self.trust_all_ssl_certificates = trust_all_ssl_certificates
        # token overrides user_id and password
        if token is not None:
            self._headers['AUTHORIZATION'] = token
        elif user_id is not None and password is not None:
            self._headers['AUTHORIZATION'] = _get_token(user_id, password)
        if self.timeout < 1:
            raise ValueError('Timeout value must be at least 1 second')

    def _call(self, method, params):
        arg_hash = {'method': method,
                    'params': params,
                    'version': '1.1',
                    'id': str(_random.random())[2:]
                    }

        body = _json.dumps(arg_hash, cls=_JSONObjectEncoder)
        ret = _requests.post(self.url, data=body, headers=self._headers,
                             timeout=self.timeout,
                             verify=not self.trust_all_ssl_certificates)
        if ret.status_code == _requests.codes.server_error:
            if _CT in ret.headers and ret.headers[_CT] == _AJ:
                err = _json.loads(ret.text)
                if 'error' in err:
                    raise ServerError(**err['error'])
                else:
                    raise ServerError('Unknown', 0, ret.text)
            else:
                raise ServerError('Unknown', 0, ret.text)
        if ret.status_code != _requests.codes.OK:
            ret.raise_for_status()
        resp = _json.loads(ret.text)
        if 'result' not in resp:
            raise ServerError('Unknown', 0, 'An unknown server error occurred')
        return resp['result']

    def ver(self):
        resp = self._call('Workspace.ver',
                          [])
        return resp[0]

    def create_workspace(self, params):
        resp = self._call('Workspace.create_workspace',
                          [params])
        return resp[0]

    def alter_workspace_metadata(self, params):
        self._call('Workspace.alter_workspace_metadata',
                   [params])

    def clone_workspace(self, params):
        resp = self._call('Workspace.clone_workspace',
                          [params])
        return resp[0]

    def lock_workspace(self, wsi):
        resp = self._call('Workspace.lock_workspace',
                          [wsi])
        return resp[0]

    def get_workspacemeta(self, params):
        resp = self._call('Workspace.get_workspacemeta',
                          [params])
        return resp[0]

    def get_workspace_info(self, wsi):
        resp = self._call('Workspace.get_workspace_info',
                          [wsi])
        return resp[0]

    def get_workspace_description(self, wsi):
        resp = self._call('Workspace.get_workspace_description',
                          [wsi])
        return resp[0]

    def set_permissions(self, params):
        self._call('Workspace.set_permissions',
                   [params])

    def set_global_permission(self, params):
        self._call('Workspace.set_global_permission',
                   [params])

    def set_workspace_description(self, params):
        self._call('Workspace.set_workspace_description',
                   [params])

    def get_permissions_mass(self, mass):
        resp = self._call('Workspace.get_permissions_mass',
                          [mass])
        return resp[0]

    def get_permissions(self, wsi):
        resp = self._call('Workspace.get_permissions',
                          [wsi])
        return resp[0]

    def save_object(self, params):
        resp = self._call('Workspace.save_object',
                          [params])
        return resp[0]

    def save_objects(self, params):
        resp = self._call('Workspace.save_objects',
                          [params])
        return resp[0]

    def get_object(self, params):
        resp = self._call('Workspace.get_object',
                          [params])
        return resp[0]

    def get_object_provenance(self, object_ids):
        resp = self._call('Workspace.get_object_provenance',
                          [object_ids])
        return resp[0]

    def get_objects(self, object_ids):
        resp = self._call('Workspace.get_objects',
                          [object_ids])
        return resp[0]

    def get_object_subset(self, sub_object_ids):
        resp = self._call('Workspace.get_object_subset',
                          [sub_object_ids])
        return resp[0]

    def get_object_history(self, object):
        resp = self._call('Workspace.get_object_history',
                          [object])
        return resp[0]

    def list_referencing_objects(self, object_ids):
        resp = self._call('Workspace.list_referencing_objects',
                          [object_ids])
        return resp[0]

    def list_referencing_object_counts(self, object_ids):
        resp = self._call('Workspace.list_referencing_object_counts',
                          [object_ids])
        return resp[0]

    def get_referenced_objects(self, ref_chains):
        resp = self._call('Workspace.get_referenced_objects',
                          [ref_chains])
        return resp[0]

    def list_workspaces(self, params):
        resp = self._call('Workspace.list_workspaces',
                          [params])
        return resp[0]

    def list_workspace_info(self, params):
        resp = self._call('Workspace.list_workspace_info',
                          [params])
        return resp[0]

    def list_workspace_objects(self, params):
        resp = self._call('Workspace.list_workspace_objects',
                          [params])
        return resp[0]

    def list_objects(self, params):
        resp = self._call('Workspace.list_objects',
                          [params])
        return resp[0]

    def get_objectmeta(self, params):
        resp = self._call('Workspace.get_objectmeta',
                          [params])
        return resp[0]

    def get_object_info(self, object_ids, includeMetadata):
        resp = self._call('Workspace.get_object_info',
                          [object_ids, includeMetadata])
        return resp[0]

    def get_object_info_new(self, params):
        resp = self._call('Workspace.get_object_info_new',
                          [params])
        return resp[0]

    def rename_workspace(self, params):
        resp = self._call('Workspace.rename_workspace',
                          [params])
        return resp[0]

    def rename_object(self, params):
        resp = self._call('Workspace.rename_object',
                          [params])
        return resp[0]

    def copy_object(self, params):
        resp = self._call('Workspace.copy_object',
                          [params])
        return resp[0]

    def revert_object(self, object):
        resp = self._call('Workspace.revert_object',
                          [object])
        return resp[0]

    def get_names_by_prefix(self, params):
        resp = self._call('Workspace.get_names_by_prefix',
                          [params])
        return resp[0]

    def hide_objects(self, object_ids):
        self._call('Workspace.hide_objects',
                   [object_ids])

    def unhide_objects(self, object_ids):
        self._call('Workspace.unhide_objects',
                   [object_ids])

    def delete_objects(self, object_ids):
        self._call('Workspace.delete_objects',
                   [object_ids])

    def undelete_objects(self, object_ids):
        self._call('Workspace.undelete_objects',
                   [object_ids])

    def delete_workspace(self, wsi):
        self._call('Workspace.delete_workspace',
                   [wsi])

    def undelete_workspace(self, wsi):
        self._call('Workspace.undelete_workspace',
                   [wsi])

    def request_module_ownership(self, mod):
        self._call('Workspace.request_module_ownership',
                   [mod])

    def register_typespec(self, params):
        resp = self._call('Workspace.register_typespec',
                          [params])
        return resp[0]

    def register_typespec_copy(self, params):
        resp = self._call('Workspace.register_typespec_copy',
                          [params])
        return resp[0]

    def release_module(self, mod):
        resp = self._call('Workspace.release_module',
                          [mod])
        return resp[0]

    def list_modules(self, params):
        resp = self._call('Workspace.list_modules',
                          [params])
        return resp[0]

    def list_module_versions(self, params):
        resp = self._call('Workspace.list_module_versions',
                          [params])
        return resp[0]

    def get_module_info(self, params):
        resp = self._call('Workspace.get_module_info',
                          [params])
        return resp[0]

    def get_jsonschema(self, type):
        resp = self._call('Workspace.get_jsonschema',
                          [type])
        return resp[0]

    def translate_from_MD5_types(self, md5_types):
        resp = self._call('Workspace.translate_from_MD5_types',
                          [md5_types])
        return resp[0]

    def translate_to_MD5_types(self, sem_types):
        resp = self._call('Workspace.translate_to_MD5_types',
                          [sem_types])
        return resp[0]

    def get_type_info(self, type):
        resp = self._call('Workspace.get_type_info',
                          [type])
        return resp[0]

    def get_all_type_info(self, mod):
        resp = self._call('Workspace.get_all_type_info',
                          [mod])
        return resp[0]

    def get_func_info(self, func):
        resp = self._call('Workspace.get_func_info',
                          [func])
        return resp[0]

    def get_all_func_info(self, mod):
        resp = self._call('Workspace.get_all_func_info',
                          [mod])
        return resp[0]

    def grant_module_ownership(self, params):
        self._call('Workspace.grant_module_ownership',
                   [params])

    def remove_module_ownership(self, params):
        self._call('Workspace.remove_module_ownership',
                   [params])

    def list_all_types(self, params):
        resp = self._call('Workspace.list_all_types',
                          [params])
        return resp[0]

    def administer(self, command):
        resp = self._call('Workspace.administer',
                          [command])
        return resp[0]
