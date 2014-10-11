def interval(value):
    def add_attribute(function):
        function.interval = value
        return function
    return add_attribute


def rule(value):
    def add_attribute(function):
        function.rule = value
        return function
    return add_attribute


def thread(value):
    def add_attribute(function):
        function.thread = value
        return function
    return add_attribute


def commands(value):
    def add_attribute(function):
        function.commands = value
        return function
    return add_attribute


def priority(value):
    def add_attribute(function):
        function.priority = value
        return function
    return add_attribute


def example(value):
    def add_attribute(function):
        function.example = value
        return function
    return add_attribute


def event(value):
    def add_attribute(function):
        function.event = value
        return function
    return add_attribute


def rate(value):
    def add_attribute(function):
        function.rate = value
        return function
    return add_attribute