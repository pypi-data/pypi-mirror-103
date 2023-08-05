import markdown

from .markdown_extension import StandaloneFigureProcessor


class PelicanFigureExtension(markdown.Extension):
    def __init__(self):
        super().__init__()

    def extendMarkdown(self, md: markdown.core.Markdown):
        md.treeprocessors.register(
            StandaloneFigureProcessor(md), "standalone_figure", 1
        )
