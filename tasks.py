"""Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
from invoke import Collection

from invokelint import _clean, dist, lint, style, test

ns = Collection()
ns.add_collection(dist)
ns.add_collection(_clean, name="clean")
ns.add_collection(lint)
ns.add_collection(style)
ns.add_collection(test)