---
name: mealie-app
description: "Generated skill for app operations. Contains 2 tools."
tags: [app]
---

### Overview
This skill handles operations related to app.

### Available Tools
- `get_startup_info`: Get Startup Info
  - **Parameters**:
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `get_app_theme`: Get App Theme
  - **Parameters**:
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
