import json
import httmock
import romanesco
import unittest
from copy import copy


class TestGirderIo(unittest.TestCase):

    def setUp(self):
        self.task = {
            "inputs": [{"name": "input", "type": "string", "format": "text"}],
            "outputs": [{"name": "out", "type": "string", "format": "text"}],
            "script": "with open (input, 'rb') as fh:\n    out = fh.read()",
            "mode": "python"
        }

    def test_girder_io(self):
        file_uploaded = []
        upload_initialized = []
        item_created = []

        @httmock.all_requests
        def girder_mock(url, request):
            api_root = '/girder/api/v1'
            self.assertEqual(request.headers['Girder-Token'], 'foo')
            self.assertEqual(url.scheme, 'http')
            self.assertTrue(url.path.startswith(api_root), url.path)
            self.assertEqual(url.netloc, 'localhost:8080')

            if url.path == api_root + '/item/item_id/files':
                return json.dumps([{
                    'name': 'test.txt',
                    '_id': 'file_id',
                    'size': 13
                }])
            elif url.path == api_root + '/item/new_item_id/files':
                return '[]'
            elif url.path == api_root + '/file/file_id/download':
                return 'file_contents'
            elif url.path == api_root + '/file' and request.method == 'POST':
                upload_initialized.append(1)
                return json.dumps({
                    '_id': 'upload_id'
                })
            elif url.path == api_root + '/item' and request.method == 'POST':
                item_created.append(1)
                return json.dumps({
                    '_id': 'new_item_id',
                    'name': 'test.txt'
                })
            elif (url.path == api_root + '/file/chunk' and
                  request.method == 'POST'):
                file_uploaded.append(1)
                return json.dumps({
                    '_id': 'new_file_id',
                    'name': 'test.txt'
                })
            else:
                raise Exception('Unexpected %s request to %s.' % (
                    request.method, url.path))

        inputs = {
            'input': {
                'mode': 'girder',
                'host': 'localhost',
                'scheme': 'http',
                'port': 8080,
                'api_root': '/girder/api/v1',
                'resource_type': 'item',
                'id': 'item_id',
                'type': 'string',
                'format': 'text',
                'name': 'test.txt',
                'token': 'foo'
            }
        }

        with httmock.HTTMock(girder_mock):
            outputs = romanesco.run(
                self.task, inputs=inputs, outputs=None, cleanup=False)
            data = outputs['out']['data']

            self.assertEquals(data, 'file_contents')

            # Now test pushing to girder
            del inputs['input']['data']
            outputs = {
                'out': {
                    'mode': 'girder',
                    'host': 'localhost',
                    'scheme': 'http',
                    'port': 8080,
                    'api_root': '/girder/api/v1',
                    'parent_type': 'folder',
                    'parent_id': 'some_folder_id',
                    'format': 'text',
                    'type': 'string',
                    'token': 'foo'
                }
            }

            # uploading to parent_type == 'folder requires 'name' for an item
            with self.assertRaises(Exception):
                romanesco.run(self.task, inputs=inputs,
                              outputs=outputs)

            # Adding name should work
            outputs['out']['name'] = 'test'
            del inputs['input']['data']
            romanesco.run(self.task, inputs=inputs,
                          outputs=outputs)

            self.assertEqual(file_uploaded, [1])
            self.assertEqual(item_created, [1])
            self.assertEqual(upload_initialized, [1])

            outputs['out']['parent_type'] = 'item'
            del outputs['out']['name']
            del inputs['input']['data']

            # uploading to parent_type == 'item' requires either
            # 'name' or 'file_name'
            with self.assertRaises(Exception):
                romanesco.run(self.task, inputs=copy(inputs), outputs=outputs)

            # uploading file to item with 'file_name'  should work
            outputs['out']['file_name'] = 'test'
            del inputs['input']['data']
            romanesco.run(self.task, inputs=copy(inputs), outputs=outputs)
            self.assertEqual(file_uploaded, [1, 1])
            self.assertEqual(item_created, [1])
            self.assertEqual(upload_initialized, [1, 1])


if __name__ == '__main__':
    unittest.main()
