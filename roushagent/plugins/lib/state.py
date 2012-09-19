#!/usr/bin/env python

import logging


class StateMachine:
    def __init__(self, state_data={}, logger = None):
        self.states = {'success': StateMachineState(terminal=True, advance=lambda x: self._return(True, x)),
                       'failure': StateMachineState(terminal=True, advance=lambda x: self._return(False, x))}
        self.current_state = 'success'
        self.state_data = state_data
        self.result = True

        self.logger = logger
        if not logger:
            self.logger = logging.getLogger()

    def _return(self, result, state):
        return (result, state, {})

    def set_state(self, state):
        self.current_state = state

    def add_state(self, name, state):
        if state in self.states:
            raise ValueError('state %s already exists' % name)

        self.states[name] = state

    def advance(self):
        if not self.current_state in self.states.keys():
            raise ValueError('no state "%s" in state machine' % state)

        self.logger.debug('Running state %s' % self.current_state)

        if self.states[self.current_state].terminal:
            return False

        # run and go
        self.result, self.state_data = self.states[self.current_state].advance(self.state_data)

        # we've run out of nodes to act on... we've filtered out all of the
        # nodes, or else we've had task failures on individual nodes such
        # that none of them are remaining.
        if len(self.state_data['nodes']) == 0:

            self.current_state = self.states[self.current_state].on_failure



        if self.result['result_code'] == 0:
            self.current_state = self.states[self.current_state].on_success
        else:
            self.current_state = self.states[self.current_state].on_failure

        self.logger.debug('Advanced state to %s as result of outcome %s' % (self.current_state, self.result))

        return True

    def run_to_completion(self):
        while self.advance():
            pass

        return (self.result, self.state_data)

class StateMachineState:
    def __init__(self, **kwargs):
        self.params = {'on_success': 'success',
                       'on_failure': 'failure',
                       'advance': self.not_implemented,
                       'terminal': False}
        self.params.update(kwargs)

    def not_implemented(self, state):
        return (False, {})

    def __getattr__(self, name):
        if not name in self.params.keys():
            raise AttributeError

        return self.params[name]
