# Operations

## Quick Mapping

- "Show my workspaces" -> `scripts/execute_action.py list_workspaces`
- "Projects in workspace" -> `scripts/execute_action.py list_projects --workspace-gid <workspace_gid>`
- "Show tasks in project" -> `scripts/execute_action.py list_tasks --project-gid <project_gid>`
- "Only open tasks" -> `scripts/execute_action.py list_tasks --project-gid <project_gid> --incomplete-only`
- "Task details" -> `scripts/execute_action.py get_task --task-gid <task_gid>`
- "Search tasks" -> `scripts/execute_action.py search_tasks --workspace-gid <workspace_gid> --text "<query>"`
- "My tasks" -> `scripts/execute_action.py my_tasks --workspace-gid <workspace_gid>`
- "Create task" -> `scripts/execute_action.py --allow-write create_task ...` (explicit approval required)
- "Mark task done" -> `scripts/execute_action.py --allow-write update_task --task-gid <task_gid> --completed true` (explicit approval required)
- "Add comment" -> `scripts/execute_action.py --allow-write add_comment --task-gid <task_gid> --text "..."` (explicit approval required)

## Typical Flow

1. Identify workspace with `scripts/execute_action.py list_workspaces`.
2. Identify project with `scripts/execute_action.py list_projects --workspace-gid <workspace_gid>`.
3. Inspect tasks with `scripts/execute_action.py list_tasks --project-gid <project_gid>`.
4. Run write actions only with explicit approval and `--allow-write`.
