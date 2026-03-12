#!/usr/bin/env python3
import argparse

import asana

import _common


def parse_args():
  parser = argparse.ArgumentParser(description='List my incomplete tasks in a workspace.')
  parser.add_argument('--workspace-gid', required=True)
  parser.add_argument('--limit', type=int, default=100)
  return parser.parse_args()


def main():
  args = parse_args()
  api_client = _common.get_client()

  try:
    me = asana.UsersApi(api_client).get_user('me', {})
  except Exception as error:
    _common.fail(str(error))

  opts = {
    'assignee': me.get('gid'),
    'workspace': args.workspace_gid,
    'completed_since': 'now',
    'opt_fields': 'name,due_on,created_at,modified_at,projects.name,memberships.section.name,memberships.project.name',
  }

  try:
    tasks = list(asana.TasksApi(api_client).get_tasks(opts, item_limit=args.limit))
  except Exception as error:
    _common.fail(str(error))

  rows = []
  for task in tasks:
    projects = task.get('projects') or []
    project_names = ', '.join(p.get('name', '') for p in projects if p.get('name'))
    sections = _common.extract_sections(task.get('memberships') or [])
    rows.append([
      _common.text(task.get('name'), 'Untitled task'),
      _common.text(task.get('due_on'), 'No date'),
      _common.format_timestamp(task.get('created_at')),
      _common.format_timestamp(task.get('modified_at')),
      _common.text(project_names, 'No project'),
      _common.text(sections, '-'),
      _common.text(task.get('gid'), 'Unknown'),
    ])

  _common.print_table(['Task', 'Due Date', 'Created', 'Updated', 'Projects', 'Column', 'Task GID'], rows)


if __name__ == '__main__':
  main()
