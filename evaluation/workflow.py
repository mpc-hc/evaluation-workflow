from trac.core import *
from trac.ticket.api import ITicketActionController, TicketSystem
from trac.ticket.default_workflow import ConfigurableTicketWorkflow
from trac.config import Option, ListOption
from trac.util.translation import _, tag_
from genshi.builder import tag


class EvaluationTicketWorkflow(Component):

    """Support for evaluation field.

    The action that supports the `set_evaluation` operation will present
    a dropdown list with different stage of evaluation.

    To install add the `EvaluationTicketWorkflow` to the workflow
    option in the `[ticket]` section in TracIni.
    If there is no other workflow option, the line will look like this:
    {{{
    workflow = ConfigurableTicketWorkflow,EvaluationTicketWorkflow
    }}}

    You can define new evaluation stages by defining `evaluation.options`
    in the `[ticket-custom]` section in TracIni. Which should look like:
    {{{
    evaluation.options = |need info|reproduced|diagnosed
    }}}
    """

    implements(ITicketActionController)

    # Set the custom field option defaults
    Option('ticket-custom', 'evaluation', 'select')
    Option('ticket-custom', 'evaluation.label', _('Evaluation'))
    Option('ticket-custom', 'evaluation.options', '|need info|reproduced|diagnosed')

    # ITicketActionController methods

    def get_ticket_actions(self, req, ticket):
        actions_we_handle = []
        if 'TICKET_MODIFY' in req.perm(ticket.resource):
            controller = ConfigurableTicketWorkflow(self.env)
            actions_we_handle += controller.get_actions_by_operation_for_req(
                req, ticket, 'set_evaluation')
            actions_we_handle += controller.get_actions_by_operation_for_req(
                req, ticket, 'del_evaluation')

        self.log.debug('evaluation handles actions: %r' % actions_we_handle)
        return actions_we_handle

    def get_all_status(self):
        pass

    def render_ticket_action_control(self, req, ticket, action):
        this_action = ConfigurableTicketWorkflow(self.env).actions[action]
        status = this_action['newstate']
        operations = this_action['operations']

        control = []  # default to nothing
        hints = []
        if 'set_evaluation' in operations:
            evaluations = self._get_evaluation_options()
            if not evaluations:
                raise TracError(_('Your workflow attempts to set an evaluation '
                                  'but none is defined (configuration issue, '
                                  'please contact your Trac admin).'))
            id = 'action_%s_evaluate_evaluation' % action
            if len(evaluations) == 1:
                evaluation = tag.input(type='hidden', id=id, name=id,
                                       value=evaluations[0])
                control.append(tag_('as %(evaluation)s',
                                    evaluation=tag(evaluations[0],
                                                   evaluation)))
                hints.append(_('The evaluation will be set to %(name)s',
                               name=evaluations[0]))
            else:
                selected_option = 1
                control.append(tag_('as %(evaluation)s',
                                    evaluation=tag.select(
                                        [tag.option(x, value=x,
                                                    selected=(x == selected_option or None))
                                            for x in evaluations],
                                        id=id, name=id)))
                hints.append(_('The evaluation will be set'))
        #if 'del_evaluation' in operations:
        #    hints.append(_('The evaluation will be deleted'))

        return (this_action['name'], tag(*control), '. '.join(hints) + '.'
                if hints else '')

    def get_ticket_changes(self, req, ticket, action):
        this_action = ConfigurableTicketWorkflow(self.env).actions[action]

        # Enforce permissions
        if not 'TICKET_MODIFY' in req.perm(ticket.resource):
            # The user does not have any of the listed permissions, so we won't
            # do anything.
            return {}

        updated = {}
        # Status changes
        status = this_action['newstate']
        if status != '*':
            updated['status'] = status

        for operation in this_action['operations']:
            if operation == 'del_evaluation':
                updated['evaluation'] = ''
            elif operation == 'set_evaluation':
                newevaluation = req.args.get('action_%s_evaluate_evaluation' %
                                             action,
                                             this_action.get('set_evaluation', '').strip())
                updated['evaluation'] = newevaluation

        return updated

    def apply_action_side_effects(self, req, ticket, action):
        pass

    # Internal methods

    def _get_evaluation_options(self):
        system = TicketSystem(self.env)
        for field in system.custom_fields:
            if field['name'] == 'evaluation':
                return field['options']
