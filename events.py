from __future__ import print_function

from protopixel import Content

content = Content("Events script")

"""
Some internal events are exposed to scripting hooks
"""


@content.events("Content", "created")
def _content_created(**kwargs):
    print("HANDLE CONTENT", kwargs)


@content.events("Fixture", "created")
def _content_created(**kwargs):
    print("HANDLE FIXTURE", kwargs)
