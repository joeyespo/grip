from flask import json

class RequestContextFactory(object):
    def __init__(self):
        self.context = {
            'headers': {
                'content-type': 'text/plain'
            },
            'data': {}
        }

        self.use_gfm = True
        self.text = ''

    def using_auth(self, user, pwd):
        self.context['auth'] = (user, pwd) if user and pwd else None
        return self

    def use_github_markdown(self, should_use):
        self.use_gfm = should_use
        return self

    def from_text(self, text):
        self.text = text
        return self

    def from_context(self, context):
        self.context['data']['context'] = context
        return self

    def build_context(self):
        if self.use_gfm:
            self.context['data']['mode'] = 'gfm'
            self.context['data']['text'] = self.text
        else:
            self.context['data'] = self.text

        return self.context

    def build_json_context(self):
        self.build_context()
        if self.use_gfm:
            self.context['data'] = json.dumps(self.context['data'])
        return self.context
