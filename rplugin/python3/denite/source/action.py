# ============================================================================
# FILE: action.py
# AUTHOR: Yusuke Otsuka <mjhd.devlion@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
from denite.kind.base import Base as BaseKind
from denite.source.base import Base


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'coc-action'
        self.kind = Kind(vim)
        self.matchers = ['matcher_fuzzy']
        self.sorters = []

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteCommand_CocHeader /\v^.*$/ containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteCommand_CocId /\v^\s\S+/ contained '
                         r'containedin=deniteCommand_CocHeader nextgroup=deniteCommand_CocTitle')

    def highlight(self):
        self.vim.command('highlight default link deniteCommand_CocId Identifier')

    def gather_candidates(self, context):
        items = self.vim.call('CocAction', 'codeActions')
        if items is None or items is 0:
            return []
        candidates = []
        for item in items:
            candidates.append({
                'word': item['title'],
                'abbr': '%s %s' % (item['clientId'], item['title']),
                'action': item,
                })

        return candidates


class Kind(BaseKind):

    def __init__(self, vim):
        super().__init__(vim)
        self.default_action = 'run'

    def action_run(self, context):
        target = context['targets'][0]
        self.vim.call('CocAction', 'doCodeAction', target['action'])
