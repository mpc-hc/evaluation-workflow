from trac.core import *
from trac.web.api import ITemplateStreamFilter
from trac.ticket.api import ITicketManipulator
from genshi.filters.transform import Transformer, StreamBuffer

class EvaluationFieldHider(Component):
    """Hides and protects evaluation field."""

    implements(ITemplateStreamFilter,ITicketManipulator)

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if filename == 'ticket.html':
            filter = Transformer('//label[@for="field-evaluation"]')
            stream |= filter.remove()
            filter = Transformer('//select[@id="field-evaluation"]')
            stream |= filter.remove()
        return stream

    # ITicketManipulator methods

    def prepare_ticket(self, req, ticket, fields, actions):
        pass

    def validate_ticket(self, req, ticket):
        if 'field_evaluation' in req.args:
            return [('evaluation', 'field is protected')]
        return []
