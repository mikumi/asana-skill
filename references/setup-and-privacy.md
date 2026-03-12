# Setup And Privacy

## Prerequisites

Run:

```bash
scripts/check_prereqs.sh
```

The check validates:

1. `python3` is installed
2. `asana` Python package is installed
3. `ASANA_ACCESS_TOKEN` is set

If token is missing:

1. Open https://app.asana.com/0/my-apps
2. Create a personal access token
3. Set it in shell config:

```bash
echo 'export ASANA_ACCESS_TOKEN="YOUR_TOKEN"' >> ~/.zshrc
source ~/.zshrc
```

## Privacy Rules

1. Default to read-only actions.
2. Run write actions only with explicit user confirmation.
3. Never echo or display the token.
4. Fetch only required fields.
5. Summarize results; avoid raw object dumps unless user asks.
