from girder.api import access
from girder.api.rest import Resource
from girder.api.describe import Description, describeRoute


class Validator(Resource):
    def __init__(self, celeryApp):
        self.resourceName = 'romanesco_validator'
        self.route('GET', (), self.find)
        self.celeryApp = celeryApp

    @access.public
    @describeRoute(
        Description('List or search for validators.')
        .param('type', 'Find validators with this type.', required=False)
        .param('format', 'Find validators with this format.', required=False)
    )
    def find(self, params):
        return self.celeryApp.send_task('romanesco.validators', [
            params.get('type', None),
            params.get('format', None)]).get()
