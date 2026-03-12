#!/usr/bin/env python3
import argparse

import asana

import _common


def parse_args():
  parser = argparse.ArgumentParser(description='Create a task in an Asana project.')
  parser.add_argument('--project-gid', required=True)
  parser.add_argument('--name', required=True)
  parser.add_argument('--notes', default='')
  return parser.parse_args()


def main():
  args = parse_args()
  api_client = _common.get_client()

  payload = {
    'name': args.name,
    'projects': [args.project_gid],
  }

  if args.notes:
    payload['notes'] = args.notes

  try:
    task = asana.TasksApi(api_client).create_task({'data': payload}, {})
  except Exception as error:
    _common.fail(str(error))

  _common.print_kv([
    ('Created', _common.text(task.get('name'), 'Untitled task')),
    ('Task GID', _common.text(task.get('gid'), 'Unknown')),
  ])


if __name__ == '__main__':
  main()
