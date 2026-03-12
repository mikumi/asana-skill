#!/usr/bin/env python3
import argparse

import asana

import _common


def parse_args():
  parser = argparse.ArgumentParser(description='List projects in an Asana workspace.')
  parser.add_argument('--workspace-gid', required=True)
  parser.add_argument('--limit', type=int, default=100)
  return parser.parse_args()


def main():
  args = parse_args()
  api_client = _common.get_client()

  opts = {
    'opt_fields': 'name,archived',
  }

  try:
    projects = list(asana.ProjectsApi(api_client).get_projects_for_workspace(args.workspace_gid, opts, item_limit=args.limit))
  except Exception as error:
    _common.fail(str(error))

  rows = []
  for project in projects:
    rows.append([
      _common.text(project.get('gid'), 'Unknown'),
      _common.text(project.get('name'), 'Unknown'),
      'Archived' if project.get('archived') else 'Active',
    ])

  _common.print_table(['Project GID', 'Project Name', 'State'], rows)


if __name__ == '__main__':
  main()
