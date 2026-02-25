[ Skip to content ](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/#permissions-and-public-access)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Permissions and Public Access
Type to start searching
[ mealie-recipes/mealie
  * v3.11.0
  * 11.5k
  * 1.1k

](https://github.com/mealie-recipes/mealie/ "Go to repository")
  * [ Home ](https://docs.mealie.io/)
  * [ Getting Started ](https://docs.mealie.io/documentation/getting-started/introduction/)
  * [ API Reference ](https://demo.mealie.io/docs)
  * [ Contributors Guide ](https://docs.mealie.io/contributors/non-coders/)
  * [ News ](https://docs.mealie.io/news/surveys/2024-october/overview/)


[ ](https://docs.mealie.io/ "Mealie") Mealie
[ mealie-recipes/mealie
  * v3.11.0
  * 11.5k
  * 1.1k

](https://github.com/mealie-recipes/mealie/ "Go to repository")
  * [ Home  ](https://docs.mealie.io/)
  * Getting Started
    * [ Introduction  ](https://docs.mealie.io/documentation/getting-started/introduction/)
    * [ Features  ](https://docs.mealie.io/documentation/getting-started/features/)
    * [ Updating  ](https://docs.mealie.io/documentation/getting-started/updating/)
    * [ Version 1 Migration  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/)
    * [ FAQ  ](https://docs.mealie.io/documentation/getting-started/faq/)
    * [ API  ](https://docs.mealie.io/documentation/getting-started/api-usage/)
    * [ Road Map  ](https://docs.mealie.io/documentation/getting-started/roadmap/)
    * Installation
      * [ Installation Checklist  ](https://docs.mealie.io/documentation/getting-started/installation/installation-checklist/)
      * [ SQLite (Recommended)  ](https://docs.mealie.io/documentation/getting-started/installation/sqlite/)
      * [ PostgreSQL  ](https://docs.mealie.io/documentation/getting-started/installation/postgres/)
      * [ Backend Configuration  ](https://docs.mealie.io/documentation/getting-started/installation/backend-config/)
      * [ Security  ](https://docs.mealie.io/documentation/getting-started/installation/security/)
      * [ Logs  ](https://docs.mealie.io/documentation/getting-started/installation/logs/)
      * [ OpenAI  ](https://docs.mealie.io/documentation/getting-started/installation/open-ai/)
    * Usage
      * [ Backup and Restoring  ](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/)
      * Permissions and Public Access  [ Permissions and Public Access  ](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/)
        * [ Customizable User Permissions  ](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/#customizable-user-permissions)
        * [ Public Recipe Access  ](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/#public-recipe-access)
    * Authentication
      * [ LDAP  ](https://docs.mealie.io/documentation/getting-started/authentication/ldap/)
      * [ OpenID Connect  ](https://docs.mealie.io/documentation/getting-started/authentication/oidc-v2/)
    * Community Guides
      * [ Bring API without internet exposure  ](https://docs.mealie.io/documentation/community-guide/bring-api/)
      * [ Automating Backups with n8n  ](https://docs.mealie.io/documentation/community-guide/n8n-backup-automation/)
      * [ Bulk Url Import  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/)
      * [ Home Assistant  ](https://docs.mealie.io/documentation/community-guide/home-assistant/)
      * [ Import Bookmarklet  ](https://docs.mealie.io/documentation/community-guide/import-recipe-bookmarklet/)
      * [ iOS Shortcut  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/)
      * [ Reverse Proxy (SWAG)  ](https://docs.mealie.io/documentation/community-guide/swag/)
  * [ API Reference  ](https://demo.mealie.io/docs)
  * Contributors Guide
    * [ Non-Code  ](https://docs.mealie.io/contributors/non-coders/)
    * [ Translating  ](https://docs.mealie.io/contributors/translating/)
    * Developers Guide
      * [ Building Packages  ](https://docs.mealie.io/contributors/developers-guide/building-packages/)
      * [ Code Contributions  ](https://docs.mealie.io/contributors/developers-guide/code-contributions/)
      * [ Dev Getting Started  ](https://docs.mealie.io/contributors/developers-guide/starting-dev-server/)
      * [ Database Changes  ](https://docs.mealie.io/contributors/developers-guide/database-changes/)
      * [ Maintainers Guide  ](https://docs.mealie.io/contributors/developers-guide/maintainers/)
      * [ Migration Guide  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/)
    * Guides
      * [ Improving Ingredient Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/)
  * News
    * Surveys
      * [ October 2024  ](https://docs.mealie.io/news/surveys/2024-october/overview/)


  * [ Customizable User Permissions  ](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/#customizable-user-permissions)
  * [ Public Recipe Access  ](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/#public-recipe-access)


# Permissions and Public Access
Mealie provides various levels of user access and permissions. This includes:
  * Authentication and registration ([LDAP](https://docs.mealie.io/documentation/getting-started/authentication/ldap/) and [OpenID Connect](https://docs.mealie.io/documentation/getting-started/authentication/oidc/) are both supported)
  * Customizable user permissions
  * Fine-tuned public access for non-users


## Customizable User Permissions
Each user can be configured to have varying levels of access. Some of these permissions include:
  * Access to Administrator tools
  * Access to inviting other users
  * Access to manage their group and group data


Administrators can configure these settings on the User Management page (navigate to Settings > Admin Settings > Users or append `/admin/manage/users` to your instance URL).
[User Management Demo](https://demo.mealie.io/admin/manage/users)
## Public Recipe Access
By default, groups and households are set to private, meaning only logged-in users may access the group/household. In order for a recipe to be viewable by public (not logged-in) users, three criteria must be met:
  1. The group must not be private
  2. The household must not be private, _and_ the household setting for allowing users outside of your group to see your recipes must be enabled. These can be toggled on the Household Management page (navigate to Settings > Admin Settings > Households or append `/admin/manage/households` to your instance URL)
  3. The recipe must be set to public. This can be toggled for each recipe individually, or in bulk using the Recipe Data Management page


Additionally, if the group is not private, public users can view all public group data (public recipes, public cookbooks, etc.) from the home page ([e.g. the demo home page](https://demo.mealie.io/g/home)).
[Group Settings Demo](https://demo.mealie.io/group)
More broadly, here are the rules for how recipe access is determined:
  * Private links that are generated from the recipe page using the `Share` button bypass all group and recipe permissions
  * Private groups block all access to recipes, including those that are public, except as noted above.
  * Private households, similar to private groups, block all access to recipes, except as noted above.
  * Households with "Allow users outside of your group to see your recipes" disabled block all access to recipes, except as noted above.
  * Private recipes block all access to the recipe from public links. This does not affect Private Links.


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
