#!/usr/bin/env python3
import asana

import _common


def main():
  api_client = _common.get_client()
  try:
    workspaces = list(asana.WorkspacesApi(api_client).get_workspaces({}))
  except Exception as error:
    _common.fail(str(error))

  rows = []
  for workspace in workspaces:
    rows.append([
      _common.text(workspace.get('gid'), 'Unknown'),
      _common.text(workspace.get('name'), 'Unknown'),
    ])

  _common.print_table(['Workspace GID', 'Workspace Name'], rows)


if __name__ == '__main__':
  main()
