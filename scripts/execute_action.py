#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


ACTIONS = {
  'current_user': {'script': 'current_user.py', 'mode': 'read'},
  'list_workspaces': {'script': 'list_workspaces.py', 'mode': 'read'},
  'list_projects': {'script': 'list_projects.py', 'mode': 'read'},
  'list_tasks': {'script': 'list_tasks.py', 'mode': 'read'},
  'get_task': {'script': 'get_task.py', 'mode': 'read'},
  'search_tasks': {'script': 'search_tasks.py', 'mode': 'read'},
  'my_tasks': {'script': 'my_tasks.py', 'mode': 'read'},
  'create_task': {'script': 'create_task.py', 'mode': 'write'},
  'update_task': {'script': 'update_task.py', 'mode': 'write'},
  'add_comment': {'script': 'add_comment.py', 'mode': 'write'},
}


def _print_usage():
  print('Usage:')
  print('  scripts/execute_action.py [--allow-write] <action> [action-args]')
  print('  scripts/execute_action.py --list-actions')
  print('')
  print('Examples:')
  print('  scripts/execute_action.py list_workspaces')
  print('  scripts/execute_action.py list_projects --workspace-gid 123')
  print('  scripts/execute_action.py --allow-write update_task --task-gid 456 --completed true')


def _print_actions():
  print('Available actions:')
  for name in sorted(ACTIONS.keys()):
    mode = ACTIONS[name]['mode']
    print(f'  - {name} ({mode})')


def _parse(argv):
  allow_write = False
  list_actions = False
  remaining = []

  for token in argv:
    if token == '--allow-write':
      allow_write = True
    elif token == '--list-actions':
      list_actions = True
    else:
      remaining.append(token)

  return allow_write, list_actions, remaining


def main():
  allow_write, list_actions, remaining = _parse(sys.argv[1:])

  if list_actions:
    _print_actions()
    return

  if not remaining or remaining[0] in ('-h', '--help'):
    _print_usage()
    return

  action = remaining[0]
  action_args = remaining[1:]

  action_config = ACTIONS.get(action)
  if action_config is None:
    print(f'ERROR: Unknown action "{action}".', file=sys.stderr)
    _print_actions()
    raise SystemExit(2)

  if action_config['mode'] == 'write' and not allow_write:
    print(
      'ERROR: Write action blocked. Re-run with --allow-write only after explicit user approval.',
      file=sys.stderr,
    )
    raise SystemExit(2)

  script_path = Path(__file__).resolve().parent / action_config['script']
  if not script_path.exists():
    print(f'ERROR: Missing script: {script_path}', file=sys.stderr)
    raise SystemExit(1)

  cmd = [sys.executable, str(script_path), *action_args]
  result = subprocess.run(cmd, check=False)
  raise SystemExit(result.returncode)


if __name__ == '__main__':
  main()
