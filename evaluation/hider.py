from trac.core import *
from trac.web.api import ITemplateStreamFilter
from genshi.filters.transform import Transformer, StreamBuffer

class EvaluationFieldHider(Component):
    """Hide evaluation field."""

    implements(ITemplateStreamFilter)
    
    # ITemplateStreamFilter methods
    
    def filter_stream(self, req, method, filename, stream, data):
        if filename == 'ticket.html':
            filter = Transformer('//label[@for="field-evaluation"]')
            stream |= filter.remove()
            filter = Transformer('//select[@id="field-evaluation"]')
            stream |= filter.remove()
        return stream
