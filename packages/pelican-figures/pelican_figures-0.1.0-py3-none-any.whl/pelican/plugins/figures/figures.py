import pelican.plugins.signals

from .extension import PelicanFigureExtension


def init_figures(sender):
    sender.settings["MARKDOWN"].setdefault("extensions", []).append(
        PelicanFigureExtension()
    )


def register():
    pelican.plugins.signals.initialized.connect(init_figures)
