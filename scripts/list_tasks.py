#!/usr/bin/env python3
import argparse

import asana

import _common


def parse_args():
  parser = argparse.ArgumentParser(description='List tasks in an Asana project.')
  parser.add_argument('--project-gid', required=True)
  parser.add_argument('--incomplete-only', action='store_true')
  parser.add_argument('--limit', type=int, default=100)
  return parser.parse_args()


def main():
  args = parse_args()
  api_client = _common.get_client()

  opts = {
    'opt_fields': 'name,completed,due_on,created_at,modified_at,assignee.name,projects.name,memberships.section.name,memberships.project.name',
  }

  if args.incomplete_only:
    opts['completed_since'] = 'now'

  try:
    tasks = list(asana.TasksApi(api_client).get_tasks_for_project(args.project_gid, opts, item_limit=args.limit))
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
