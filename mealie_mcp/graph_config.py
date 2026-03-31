"""Mealie graph configuration — tag prompts and env var mappings.

This is the only file needed to enable graph mode for this agent.
Provides TAG_PROMPTS and TAG_ENV_VARS for create_graph_agent_server().
"""

                                                                       
TAG_PROMPTS: dict[str, str] = {
    "admin": (
        "You are a Mealie Admin specialist. Help users manage and interact with Admin functionality using the available tools."
    ),
    "app": (
        "You are a Mealie App specialist. Help users manage and interact with App functionality using the available tools."
    ),
    "explore": (
        "You are a Mealie Explore specialist. Help users manage and interact with Explore functionality using the available tools."
    ),
    "groups": (
        "You are a Mealie Groups specialist. Help users manage and interact with Groups functionality using the available tools."
    ),
    "households": (
        "You are a Mealie Households specialist. Help users manage and interact with Households functionality using the available tools."
    ),
    "organizer": (
        "You are a Mealie Organizer specialist. Help users manage and interact with Organizer functionality using the available tools."
    ),
    "recipes": (
        "You are a Mealie Recipes specialist. Help users manage and interact with Recipes functionality using the available tools."
    ),
    "shared": (
        "You are a Mealie Shared specialist. Help users manage and interact with Shared functionality using the available tools."
    ),
    "users": (
        "You are a Mealie Users specialist. Help users manage and interact with Users functionality using the available tools."
    ),
    "utils": (
        "You are a Mealie Utils specialist. Help users manage and interact with Utils functionality using the available tools."
    ),
}


                                                                        
TAG_ENV_VARS: dict[str, str] = {
    "admin": "ADMINTOOL",
    "app": "APPTOOL",
    "explore": "EXPLORETOOL",
    "groups": "GROUPSTOOL",
    "households": "HOUSEHOLDSTOOL",
    "organizer": "ORGANIZERTOOL",
    "recipes": "RECIPESTOOL",
    "shared": "SHAREDTOOL",
    "users": "USERSTOOL",
    "utils": "UTILSTOOL",
}
