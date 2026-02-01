---
name: mealie-recipes
description: "Generated skill for recipes operations. Contains 12 tools."
---

### Overview
This skill handles operations related to recipes.

### Available Tools
- `get_foods`: Get All
  - **Parameters**:
    - `search` (Any)
    - `order_by` (Any)
    - `order_by_null_position` (Any)
    - `order_direction` (Any)
    - `query_filter` (Any)
    - `pagination_seed` (Any)
    - `page` (int)
    - `per_page` (int)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `post_foods`: Create One
  - **Parameters**:
    - `data` (Dict)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `put_foods_merge`: Merge One
  - **Parameters**:
    - `data` (Dict)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `get_foods_item_id`: Get One
  - **Parameters**:
    - `item_id` (str)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `put_foods_item_id`: Update One
  - **Parameters**:
    - `item_id` (str)
    - `data` (Dict)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `delete_foods_item_id`: Delete One
  - **Parameters**:
    - `item_id` (str)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `get_units`: Get All
  - **Parameters**:
    - `search` (Any)
    - `order_by` (Any)
    - `order_by_null_position` (Any)
    - `order_direction` (Any)
    - `query_filter` (Any)
    - `pagination_seed` (Any)
    - `page` (int)
    - `per_page` (int)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `post_units`: Create One
  - **Parameters**:
    - `data` (Dict)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `put_units_merge`: Merge One
  - **Parameters**:
    - `data` (Dict)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `get_units_item_id`: Get One
  - **Parameters**:
    - `item_id` (str)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `put_units_item_id`: Update One
  - **Parameters**:
    - `item_id` (str)
    - `data` (Dict)
    - `accept_language` (Any)
    - `mealie_base_url` (str)
    - `mealie_token` (Optional[str])
    - `mealie_verify` (bool)
- `delete_units_item_id`: Delete One
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
