import girder_client
import os
import romanesco

from six import StringIO


def _init_client(spec, require_token=False):
    if 'api_url' in spec:
        client = girder_client.GirderClient(apiUrl=spec['api_url'])
    elif 'host' in spec:
        scheme = spec.get('scheme', 'http')
        port = spec.get('port', {
            'http': 80,
            'https': 443
        }[scheme])
        api_root = spec.get('api_root', '/api/v1')
        client = girder_client.GirderClient(
            host=spec['host'], scheme=scheme, apiRoot=api_root, port=port)

    if 'token' in spec:
        client.token = spec['token']
    elif require_token:
        raise Exception('You must pass a token for Girder authentication.')
    else:
        raise Exception('You must pass either an api_url or host key for '
                        'Girder input and output bindings.')

    return client


def fetch_handler(spec, **kwargs):
    resource_type = spec.get('resource_type', 'file').lower()
    taskInput = kwargs.get('task_input', {})
    target = taskInput.get('target', 'filepath')

    if 'id' not in spec:
        raise Exception('Must pass a resource ID for girder inputs.')
    if 'name' not in spec:
        raise Exception('Must pass a name for girder inputs.')

    client = _init_client(spec)
    dest = os.path.join(kwargs['_tempdir'], spec['name'])

    if resource_type == 'folder':
        client.downloadFolderRecursive(spec['id'], dest)
    elif resource_type == 'item':
        client.downloadItem(spec['id'], kwargs['_tempdir'], spec['name'])
    elif resource_type == 'file':
        client.downloadFile(spec['id'], dest)
    else:
        raise Exception('Invalid resource type: ' + resource_type)

    if target == 'filepath':
        return dest
    elif target == 'memory':
        with open(dest, 'rb') as fd:
            return fd.read()
    else:
        raise Exception('Invalid Girder push target: ' + target)


def push_handler(data, spec, **kwargs):
    reference = getattr(kwargs.get('_job_manager'), 'reference', None)
    parent_type = spec.get('parent_type', 'folder')
    taskOutput = kwargs.get('task_output', {})
    target = taskOutput.get('target', 'filepath')

    if 'parent_id' not in spec:
        raise Exception('Must pass parent ID for girder outputs.')

    client = _init_client(spec, require_token=True)

    if target == 'memory':
        if not spec.get('name'):
            raise Exception('Girder uploads from memory objects must '
                            'explicitly pass a "name" field.')
        fd = StringIO(data)
        client.uploadFile(parentId=spec['parent_id'], stream=fd, size=len(data),
                          parentType=parent_type, name=spec['name'],
                          reference=reference)
    elif target == 'filepath':
        name = spec.get('name') or os.path.basename(data)
        size = os.path.getsize(data)
        with open(data, 'rb') as fd:
            client.uploadFile(parentId=spec['parent_id'], stream=fd, size=size,
                              parentType=parent_type, name=name,
                              reference=reference)
    else:
        raise Exception('Invalid Girder push target: ' + target)


def load(params):
    romanesco.io.register_fetch_handler('girder', fetch_handler)
    romanesco.io.register_push_handler('girder', push_handler)
