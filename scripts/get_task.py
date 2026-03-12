#!/usr/bin/env python3
import argparse

import asana

import _common


TASK_OPT_FIELDS = ','.join([
  'name', 'notes', 'completed', 'completed_at', 'completed_by.name',
  'due_on', 'start_on', 'created_at', 'modified_at',
  'assignee.name', 'created_by.name', 'followers.name',
  'projects.name', 'memberships.section.name', 'memberships.project.name',
  'tags.name',
  'custom_fields.name', 'custom_fields.display_value',
  'parent.name', 'num_subtasks', 'num_likes',
  'permalink_url',
])

STORY_OPT_FIELDS = 'resource_subtype,text,created_at,created_by.name'

ATTACHMENT_OPT_FIELDS = 'name,resource_subtype,host,view_url,permanent_url,created_at'

SUBTASK_OPT_FIELDS = 'name,completed'


def parse_args():
  parser = argparse.ArgumentParser(description='Get details for one Asana task.')
  parser.add_argument('--task-gid', required=True)
  return parser.parse_args()


# ========== Private ==========

def _format_custom_fields(fields):
  if not fields:
    return None
  parts = []
  for cf in fields:
    name = cf.get('name', '')
    value = cf.get('display_value')
    if value:
      parts.append(f'{name}: {value}')
  return '; '.join(parts) if parts else None


def _format_subtasks(subtasks):
  if not subtasks:
    return None
  lines = []
  for st in subtasks:
    marker = '[x]' if st.get('completed') else '[ ]'
    lines.append(f'  {marker} {_common.text(st.get("name"), "Untitled")}')
  return '\n' + '\n'.join(lines)


def _format_comments(stories):
  comments = [s for s in stories if s.get('resource_subtype') == 'comment_added']
  if not comments:
    return None
  lines = []
  for c in comments:
    author = (c.get('created_by') or {}).get('name', 'Unknown')
    timestamp = _common.format_timestamp(c.get('created_at'))
    text = _common.text(c.get('text'), '(empty)')
    lines.append(f'  [{timestamp}] {author}: {text}')
  return '\n' + '\n'.join(lines)


def _format_attachments(attachments):
  if not attachments:
    return None
  lines = []
  for a in attachments:
    name = _common.text(a.get('name'), 'Untitled')
    host = a.get('host') or ''
    url = a.get('view_url') or a.get('permanent_url') or ''
    subtype = a.get('resource_subtype') or ''
    label = name
    if host:
      label = f'[{host}] {name}'
    if subtype == 'external' and not host:
      label = f'[link] {name}'
    if url:
      label = f'{label} ({url})'
    lines.append(f'  - {label}')
  return '\n' + '\n'.join(lines)


def main():
  args = parse_args()
  api_client = _common.get_client()
  tasks_api = asana.TasksApi(api_client)

  try:
    task = tasks_api.get_task(args.task_gid, {'opt_fields': TASK_OPT_FIELDS})
  except Exception as error:
    _common.fail(str(error))

  subtasks = []
  if (task.get('num_subtasks') or 0) > 0:
    try:
      subtasks = list(tasks_api.get_subtasks_for_task(args.task_gid, {'opt_fields': SUBTASK_OPT_FIELDS}))
    except Exception:
      pass

  stories = []
  try:
    stories = list(asana.StoriesApi(api_client).get_stories_for_task(args.task_gid, {'opt_fields': STORY_OPT_FIELDS}))
  except Exception:
    pass

  attachments = []
  try:
    attachments = list(asana.AttachmentsApi(api_client).get_attachments_for_object(
      args.task_gid, {'opt_fields': ATTACHMENT_OPT_FIELDS},
    ))
  except Exception:
    pass

  assignee = (task.get('assignee') or {}).get('name')
  created_by = (task.get('created_by') or {}).get('name')
  completed_by = (task.get('completed_by') or {}).get('name')
  parent = (task.get('parent') or {}).get('name')
  projects = task.get('projects') or []
  project_names = ', '.join(p.get('name', '') for p in projects if p.get('name'))
  sections = _common.extract_sections(task.get('memberships') or [])
  tags = task.get('tags') or []
  tag_names = ', '.join(t.get('name', '') for t in tags if t.get('name'))
  followers = task.get('followers') or []
  follower_names = ', '.join(f.get('name', '') for f in followers if f.get('name'))
  custom_fields_text = _format_custom_fields(task.get('custom_fields'))

  entries = [
    ('Name', _common.text(task.get('name'), 'Untitled task')),
    ('Status', 'Done' if task.get('completed') else 'Open'),
  ]

  if task.get('completed'):
    entries.append(('Completed At', _common.format_timestamp(task.get('completed_at'))))
    if completed_by:
      entries.append(('Completed By', completed_by))

  entries += [
    ('Due', _common.text(task.get('due_on'), 'No date')),
    ('Start', _common.text(task.get('start_on'), 'No date')),
    ('Created', _common.format_timestamp(task.get('created_at'))),
    ('Updated', _common.format_timestamp(task.get('modified_at'))),
    ('Created By', _common.text(created_by, 'Unknown')),
    ('Assignee', _common.text(assignee, 'Unassigned')),
    ('Followers', _common.text(follower_names, 'None')),
    ('Projects', _common.text(project_names, 'None')),
    ('Column', _common.text(sections, '-')),
    ('Tags', _common.text(tag_names, 'None')),
  ]

  if parent:
    entries.append(('Parent Task', parent))

  if custom_fields_text:
    entries.append(('Custom Fields', custom_fields_text))

  entries += [
    ('Likes', str(task.get('num_likes', 0))),
    ('URL', _common.text(task.get('permalink_url'), 'Unavailable')),
    ('Notes', _common.text(task.get('notes'), 'None')),
  ]

  subtask_text = _format_subtasks(subtasks)
  if subtask_text:
    entries.append(('Subtasks', subtask_text))

  attachment_text = _format_attachments(attachments)
  if attachment_text:
    entries.append(('Attachments', attachment_text))

  comment_text = _format_comments(stories)
  if comment_text:
    entries.append(('Comments', comment_text))

  _common.print_kv(entries)


if __name__ == '__main__':
  main()
