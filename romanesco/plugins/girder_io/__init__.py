import girder_client
import six
import os
import romanesco

def _init_client(spec, require_token=False):
    if 'host' not in spec:
        raise Exception('Host key required for girder fetch mode')

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
        raise Exception('You must pass a token for girder authentication.')

    return client


def fetch_handler(spec, **kwargs):
    resource_type = spec.get('resource_type', 'file').lower()

    if 'id' not in spec:
        raise Exception('Must pass a resource ID for girder inputs.')
    if 'name' not in spec:
        raise Exception('Must pass a name for girder inputs.')

    client = _init_client(spec)
    dest = os.path.join(kwargs['_tmp_dir'], spec['name'])

    if resource_type == 'folder':
        client.downloadFolderRecursive(spec['id'], dest)
    elif resource_type == 'item':
        client.downloadItem(spec['id'], kwargs['_tmp_dir'], spec['name'])
    elif resource_type == 'file':
        client.downloadFile(spec['id'], dest)
    else:
        raise Exception('Invalid resource type: ' + resource_type)

    return dest


def push_handler(data, spec, **kwargs):
    parent_type = spec.get('parent_type', 'folder')

    # Get the size of the BytesIO stream by seeking to the
    # end,  calling tell() and then seeking to the begining
    data = six.BytesIO(data)
    data.seek(0, os.SEEK_END)
    size = data.tell()
    data.seek(0)

    client = _init_client(spec, require_token=True)

    if 'parent_id' not in spec:
        raise Exception('Must pass parent ID for girder outputs.')

    if parent_type == 'folder':
        if 'name' not in spec:
            raise Exception('Must pass an item name for girder '
                            'folder outputs.')

        item = client.createItem(
            spec['parent_id'], spec['name'],
            description=spec.get('description'))

        client.uploadFile(item['_id'], data,
                          spec.get('file_name', spec['name']), size)

    elif parent_type == 'item':
        if 'file_name' not in spec and 'name' not in spec:
            raise Exception('Must pass a file name for girder item outputs.')

        client.uploadFile(spec['parent_id'], data,
                          spec.get('file_name', spec['name']), size)
    else:
        raise Exception('Invalid parent type: ' + parent_type)


def load(params):
    romanesco.io.register_fetch_handler('girder', fetch_handler)
    romanesco.io.register_push_handler('girder', push_handler)
