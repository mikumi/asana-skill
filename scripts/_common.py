#!/usr/bin/env python3
import sys
import os


def fail(message, code=1):
  print(f'ERROR: {message}', file=sys.stderr)
  raise SystemExit(code)


def get_client():
  token = os.environ.get('ASANA_ACCESS_TOKEN')
  if not token:
    fail('ASANA_ACCESS_TOKEN is not set. Run scripts/check_prereqs.sh first.', 2)

  try:
    import asana
  except ImportError:
    fail('Python package "asana" is not installed. Install with: pip3 install asana', 2)

  configuration = asana.Configuration()
  configuration.access_token = token
  return asana.ApiClient(configuration)


def text(value, fallback=''):
  if value is None:
    return fallback
  value = str(value).strip()
  if not value:
    return fallback
  return value


def format_timestamp(value):
  if not value:
    return '-'
  return value.replace('T', ' ').replace('Z', '').rsplit('.', 1)[0]


def extract_sections(memberships):
  parts = []
  for m in memberships:
    section = (m.get('section') or {}).get('name')
    if section:
      parts.append(section)
  return ', '.join(parts)


def print_kv(entries):
  for key, value in entries:
    print(f'{key}: {value}')


def print_table(headers, rows):
  normalized_rows = [[text(cell, '') for cell in row] for row in rows]
  if not normalized_rows:
    print('(no results)')
    return

  widths = [len(header) for header in headers]
  for row in normalized_rows:
    for index, cell in enumerate(row):
      if len(cell) > widths[index]:
        widths[index] = len(cell)

  divider = '+{}+'.format('+'.join('-' * (width + 2) for width in widths))

  def format_row(values):
    parts = []
    for index, value in enumerate(values):
      parts.append(f' {value.ljust(widths[index])} ')
    return '|{}|'.format('|'.join(parts))

  print(divider)
  print(format_row(headers))
  print(divider)
  for row in normalized_rows:
    print(format_row(row))
  print(divider)
