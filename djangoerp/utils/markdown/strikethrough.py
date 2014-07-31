"""
Adds the possibility to use "~~something~~" to create a span that looks like <del>something</del>
"""

from markdown.inlinepatterns import SimpleTagPattern
from markdown.extensions import Extension


class StrikeThroughExtension(Extension):

    RE = r'(~{2})([^~]+?)(~{2})'

    def extendMarkdown(self, md, md_globals):  # noqa
        """Modifies inline patterns."""
        del_tag = SimpleTagPattern(self.RE, 'del')
        md.inlinePatterns.add('del', del_tag, '_begin')
