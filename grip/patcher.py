import re


INCOMPLETE_TASK_RE = re.compile(r'<li>\[ \] (.*?)(<ul.*?>|</li>)', re.DOTALL)
INCOMPLETE_TASK_SUB = (r'<li class="task-list-item">'
                       r'<input type="checkbox" '
                       r'class="task-list-item-checkbox" disabled=""> \1\2')
COMPLETE_TASK_RE = re.compile(r'<li>\[x\] (.*?)(<ul.*?>|</li>)', re.DOTALL)
COMPLETE_TASK_SUB = (r'<li class="task-list-item">'
                     r'<input type="checkbox" class="task-list-item-checkbox" '
                     r'checked="" disabled=""> \1\2')


def patch(html, user_content=False):
    """
    Processes the HTML rendered by the GitHub API, patching
    any inconsistencies from the main site.
    """
    # FUTURE: Remove this once GitHub API renders task lists
    # https://github.com/isaacs/github/issues/309
    if not user_content:
        html = INCOMPLETE_TASK_RE.sub(INCOMPLETE_TASK_SUB, html)
        html = COMPLETE_TASK_RE.sub(COMPLETE_TASK_SUB, html)

    return html
