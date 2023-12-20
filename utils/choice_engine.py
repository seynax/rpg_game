from random import *

def append_various_data(source, destination):
    if isinstance(source, list) and isinstance(destination, dict):
        i = 0
        for value in source:
            destination[i] = value
            i += 1
        return
    elif isinstance(source, dict) and isinstance(destination, dict):
        for key, value in source:
            destination[key] = value
        return
    elif isinstance(source, list) and isinstance(destination, list):
        for value in source:
            destination.append(value)
        return
    destination = source

class Parameters:
    def __init__(self):
        self.parameters = []

    def add(self, parameter):
        self.parameters.append(parameter)

    def reset(self):
        self.parameters.clear()

class Results:
    def __init__(self):
        self.input_parameters   = []
        self.output_parameters  = Parameters()
        self.messages           = []
        self.results            = []
        self.states             = []
        self.last_state         = -1

    def reset(self):
        self.states             .clear()
        self.last_state         = -1
        self.output_parameters  .reset()
        self.results            .clear()

    def add_states(self, states):
        append_various_data(states, self.states)
        self.last_state = states

    def add_input_parameters(self, input_parameters):
        append_various_data(input_parameters, self.input_parameters)

    def add_output_parameters(self, output_parameters):
        self.output_parameters.add()

    def add_messages(self, messages):
        append_various_data(messages, self.messages)

    def add_results(self, results):
        append_various_data(results, self.results)

class Choices:
    def __init__(self, choices=None):
        self.choices    = []
        append_various_data(self.results, choices)
        self.results    = Results()

def make_choice(condition=None, message=None, execution=None, exit=False, state=-1):
    choice = {}

    choice["condition"]     = condition
    choice["execution"]     = execution
    choice["message"]       = message
    choice["exit"]          = exit
    choice["state"]         = state
    choice["parameters"]    = Parameters()

    return choice

def multiple_choices(value, choice_array):
    result = Results()
    for choice in choice_array:
        (conditionExists, condition) = exists("condition", choice)
        if conditionExists and condition(value):
            (executionExists,   execution)  = exists("execution", choice)
            (parametersExists,  parameters) = exists("parameters", choice)
            if executionExists:
                parameters.add(execution(value, parameters))

            (messageExists, message)        = exists("message", choice)
            if messageExists:
                if isinstance(message, str):
                    content = message
                else:
                    content = message(value, parameters)

                if content != None and isinstance(content, str):
                    content = content.replace("%v", str(value))
                    i = 0
                    for parameter in parameters.parameters:
                        if(isinstance(parameter, tuple)):
                            i0 = 0
                            for sub_parameter in parameter:
                                content = content.replace("%p" + str(i + i0), str(sub_parameter))
                                i0 += 1
                        else:
                            content = content.replace("%p" + str(i), str(parameter))
                        i += 1

                    print(content)
                else:
                    print(str(content))

            (exitExists,    exit)   = exists("exit", choice)
            (stateExists,   state)  = exists("state", choice)
            if exitExists and exit:
                states.append(state)
                return (state, states)
    return (None, states)

def multiple_choices_index(value, parameters):
    choices = []
    i       = 0
    for parameter in parameters:
        if isinstance(parameter, str):
            choices.append(make_choice(f_equal(i), parameter))
        elif isinstance(parameter, dict):
            parameter["condition"] = f_equal(i)
            choices.append(parameter)
        i += 1
    return multiple_choices(value, choices)

def rand_multiple_choices(min, max, choices):
    return multiple_choices(randint(min, max), choices)

def rand_multiple_choices_index(min, max, parameters):
    return multiple_choices_index(randint(min, max), parameters)

def f_not_zero():
    return lambda value: value != 0

def f_lower(toValue):
    return lambda value: value < toValue

def f_lower_equal(toValue):
    return lambda value: value <= toValue

def f_upper_equal(toValue):
    return lambda value: value >= toValue

def f_upper(toValue):
    return lambda value: value > toValue

def f_equal(toValue):
    return lambda value: value == toValue

def ret(value):
    return value

def exists(key, array):
    if(key not in array):
        return (False, None)

    value = array[key]

    return (value != None, value)