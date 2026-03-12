#!/usr/bin/env python3
import argparse

import asana

import _common


def parse_args():
  parser = argparse.ArgumentParser(description='Update fields on an Asana task.')
  parser.add_argument('--task-gid', required=True)
  parser.add_argument('--name')
  parser.add_argument('--notes')
  parser.add_argument('--due-on')
  parser.add_argument('--assignee-gid')
  parser.add_argument('--completed', choices=['true', 'false'])
  return parser.parse_args()


def main():
  args = parse_args()
  api_client = _common.get_client()

  payload = {}
  if args.name is not None:
    payload['name'] = args.name
  if args.notes is not None:
    payload['notes'] = args.notes
  if args.due_on is not None:
    payload['due_on'] = args.due_on
  if args.assignee_gid is not None:
    payload['assignee'] = args.assignee_gid
  if args.completed is not None:
    payload['completed'] = args.completed == 'true'

  if not payload:
    _common.fail('Provide at least one update flag (for example: --completed true).', 2)

  try:
    asana.TasksApi(api_client).update_task({'data': payload}, args.task_gid, {})
  except Exception as error:
    _common.fail(str(error))

  _common.print_kv([
    ('Updated Task', args.task_gid),
    ('Changed Fields', ', '.join(sorted(payload.keys()))),
  ])


if __name__ == '__main__':
  main()
