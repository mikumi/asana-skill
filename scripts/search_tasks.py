#!/usr/bin/env python3
import argparse

import asana

import _common


def parse_args():
  parser = argparse.ArgumentParser(description='Search tasks within a workspace.')
  parser.add_argument('--workspace-gid', required=True)
  parser.add_argument('--text', required=True)
  parser.add_argument('--limit', type=int, default=50)
  return parser.parse_args()


def main():
  args = parse_args()
  api_client = _common.get_client()

  opts = {
    'text': args.text,
    'opt_fields': 'name,completed,due_on,created_at,modified_at,assignee.name,projects.name,memberships.section.name,memberships.project.name',
  }

  try:
    tasks = list(asana.TasksApi(api_client).search_tasks_for_workspace(args.workspace_gid, opts, item_limit=args.limit))
  except Exception as error:
    _common.fail(str(error))

  rows = []
  for task in tasks:
    assignee = task.get('assignee') or {}
    projects = task.get('projects') or []
    project_names = ', '.join(p.get('name', '') for p in projects if p.get('name'))
    sections = _common.extract_sections(task.get('memberships') or [])
    rows.append([
      _common.text(task.get('name'), 'Untitled task'),
      'Done' if task.get('completed') else 'Open',
      _common.text(task.get('due_on'), 'No date'),
      _common.format_timestamp(task.get('created_at')),
      _common.format_timestamp(task.get('modified_at')),
      _common.text(assignee.get('name'), 'Unassigned'),
      _common.text(project_names, 'No project'),
      _common.text(sections, '-'),
      _common.text(task.get('gid'), 'Unknown'),
    ])

  _common.print_table(['Task', 'Status', 'Due Date', 'Created', 'Updated', 'Assignee', 'Projects', 'Column', 'Task GID'], rows)


if __name__ == '__main__':
  main()
