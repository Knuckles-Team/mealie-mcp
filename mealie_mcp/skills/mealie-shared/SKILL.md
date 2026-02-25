---
name: mealie-shared
description: "Generated skill for shared operations. Contains 4 tools."
tags: [shared]
---

### Overview
This skill handles operations related to shared.

### Available Tools
- `get_shared_recipes`: Get All
  - **Parameters**:
    - `recipe_id` (Any)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `post_shared_recipes`: Create One
  - **Parameters**:
    - `data` (Dict)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `get_shared_recipes_item_id`: Get One
  - **Parameters**:
    - `item_id` (str)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `delete_shared_recipes_item_id`: Delete One
  - **Parameters**:
    - `item_id` (str)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
