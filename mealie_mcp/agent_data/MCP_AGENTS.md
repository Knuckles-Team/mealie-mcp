# MCP_AGENTS.md - Dynamic Agent Registry

This file tracks the generated agents from MCP servers. You can manually modify the 'Tools' list to customize agent expertise.

## Agent Mapping Table

| Name | Description | System Prompt | Tools | Tag | Source MCP |
|------|-------------|---------------|-------|-----|------------|
| Mealie Groups Specialist | Expert specialist for groups domain tasks. | You are a Mealie Groups specialist. Help users manage and interact with Groups functionality using the available tools. | mealie-mcp_groups_toolset | groups | mealie-mcp |
| Mealie Admin Specialist | Expert specialist for admin domain tasks. | You are a Mealie Admin specialist. Help users manage and interact with Admin functionality using the available tools. | mealie-mcp_admin_toolset | admin | mealie-mcp |
| Mealie Users Specialist | Expert specialist for users domain tasks. | You are a Mealie Users specialist. Help users manage and interact with Users functionality using the available tools. | mealie-mcp_users_toolset | users | mealie-mcp |
| Mealie Organizer Specialist | Expert specialist for organizer domain tasks. | You are a Mealie Organizer specialist. Help users manage and interact with Organizer functionality using the available tools. | mealie-mcp_organizer_toolset | organizer | mealie-mcp |
| Mealie Households Specialist | Expert specialist for households domain tasks. | You are a Mealie Households specialist. Help users manage and interact with Households functionality using the available tools. | mealie-mcp_households_toolset | households | mealie-mcp |
| Mealie Explore Specialist | Expert specialist for explore domain tasks. | You are a Mealie Explore specialist. Help users manage and interact with Explore functionality using the available tools. | mealie-mcp_explore_toolset | explore | mealie-mcp |
| Mealie Recipes Specialist | Expert specialist for recipes domain tasks. | You are a Mealie Recipes specialist. Help users manage and interact with Recipes functionality using the available tools. | mealie-mcp_recipes_toolset | recipes | mealie-mcp |
| Mealie Utils Specialist | Expert specialist for utils domain tasks. | You are a Mealie Utils specialist. Help users manage and interact with Utils functionality using the available tools. | mealie-mcp_utils_toolset | utils | mealie-mcp |
| Mealie Shared Specialist | Expert specialist for shared domain tasks. | You are a Mealie Shared specialist. Help users manage and interact with Shared functionality using the available tools. | mealie-mcp_shared_toolset | shared | mealie-mcp |
| Mealie App Specialist | Expert specialist for app domain tasks. | You are a Mealie App specialist. Help users manage and interact with App functionality using the available tools. | mealie-mcp_app_toolset | app | mealie-mcp |
| Mealie Misc Specialist | Expert specialist for misc domain tasks. | You are a Mealie Misc specialist. Help users manage and interact with Misc functionality using the available tools. | mealie-mcp_misc_toolset | misc | mealie-mcp |

## Tool Inventory Table

| Tool Name | Description | Tag | Source |
|-----------|-------------|-----|--------|
| mealie-mcp_groups_toolset | Static hint toolset for groups based on config env. | groups | mealie-mcp |
| mealie-mcp_admin_toolset | Static hint toolset for admin based on config env. | admin | mealie-mcp |
| mealie-mcp_users_toolset | Static hint toolset for users based on config env. | users | mealie-mcp |
| mealie-mcp_organizer_toolset | Static hint toolset for organizer based on config env. | organizer | mealie-mcp |
| mealie-mcp_households_toolset | Static hint toolset for households based on config env. | households | mealie-mcp |
| mealie-mcp_explore_toolset | Static hint toolset for explore based on config env. | explore | mealie-mcp |
| mealie-mcp_recipes_toolset | Static hint toolset for recipes based on config env. | recipes | mealie-mcp |
| mealie-mcp_utils_toolset | Static hint toolset for utils based on config env. | utils | mealie-mcp |
| mealie-mcp_shared_toolset | Static hint toolset for shared based on config env. | shared | mealie-mcp |
| mealie-mcp_app_toolset | Static hint toolset for app based on config env. | app | mealie-mcp |
| mealie-mcp_misc_toolset | Static hint toolset for misc based on config env. | misc | mealie-mcp |
