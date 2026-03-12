#!/usr/bin/env python3
import asana

import _common


def main():
  api_client = _common.get_client()
  try:
    user = asana.UsersApi(api_client).get_user('me', {})
  except Exception as error:
    _common.fail(str(error))

  _common.print_kv([
    ('Name', _common.text(user.get('name'), 'Unknown')),
    ('Email', _common.text(user.get('email'), 'Unknown')),
    ('GID', _common.text(user.get('gid'), 'Unknown')),
  ])


if __name__ == '__main__':
  main()
