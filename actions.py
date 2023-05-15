import inspect


class Actions:
    def __init__(self):
        self.actions = {}


    def register_action(self, func):
        name = func.__name__
        self.actions[name] = func


    def context(self) -> str:
        descs = []
        for key, value in self.actions.items():
            args = inspect.signature(value).parameters
            doc = inspect.getdoc(value)
            text = key + "(" + ', '.join(args) + ")"
            if doc:
                text += "\n" + doc
            descs.append(text)
        return '\n'.join(descs)
    

    def call(self, signature: str) -> str:
        return eval(signature, dict(self.actions), None)
