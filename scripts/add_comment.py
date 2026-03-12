#!/usr/bin/env python3
import argparse

import asana

import _common


def parse_args():
  parser = argparse.ArgumentParser(description='Add a comment to an Asana task.')
  parser.add_argument('--task-gid', required=True)
  parser.add_argument('--text', required=True)
  return parser.parse_args()


def main():
  args = parse_args()
  api_client = _common.get_client()

  try:
    comment = asana.StoriesApi(api_client).create_story_for_task({'data': {'text': args.text}}, args.task_gid, {})
  except Exception as error:
    _common.fail(str(error))

  _common.print_kv([
    ('Comment Added To Task', args.task_gid),
    ('Story GID', _common.text(comment.get('gid'), 'Unknown')),
  ])


if __name__ == '__main__':
  main()
