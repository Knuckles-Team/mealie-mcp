[ Skip to content ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#migration-guide)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Migration Guide
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
      * [ Permissions and Public Access  ](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/)
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
      * Migration Guide  [ Migration Guide  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/)
        * [ V1 → V2  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#v1-v2)
          * [ updateAt is now updatedAt  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#updateat-is-now-updatedat)
          * [ Backend Endpoint Changes  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#backend-endpoint-changes)
          * [ Frontend Links  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#frontend-links)
    * Guides
      * [ Improving Ingredient Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/)
  * News
    * Surveys
      * [ October 2024  ](https://docs.mealie.io/news/surveys/2024-october/overview/)


  * [ V1 → V2  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#v1-v2)
    * [ updateAt is now updatedAt  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#updateat-is-now-updatedat)
    * [ Backend Endpoint Changes  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#backend-endpoint-changes)
    * [ Frontend Links  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/#frontend-links)


# Migration Guide
This guide is a reference for developers maintaining custom integrations with Mealie. While we aim to keep breaking changes to a minimum, major versions are likely to contain at least _some_ breaking changes. To clarify: _most users do not need to worry about this, this is_ _only_ _for those maintaining integrations and/or leveraging the API_.
While this guide aims to simplify the migration process for developers, it's not necessarily a comprehensive list of breaking changes. Starting with v2, a comprehensive list of breaking changes are highlighted in the release notes.
## V1 → V2
The biggest change between V1 and V2 is the introduction of Households. For more information on how households work in relation to groups/users, check out the [Groups and Households](https://docs.mealie.io/documentation/getting-started/features/#groups-and-households) section in the Features guide.
###  `updateAt` is now `updatedAt`
We have renamed the `updateAt` field to `updatedAt`. While the API will still accept `updateAt` as an alias, the API will return it as `updatedAt`. The field's behavior has otherwise been unchanged.
### Backend Endpoint Changes
These endpoints have moved, but are otherwise unchanged:
  * `/recipes/create-url` -> `/recipes/create/url`
  * `/recipes/create-url/bulk` -> `/recipes/create/url/bulk`
  * `/recipes/create-from-zip` -> `/recipes/create/zip`
  * `/recipes/create-from-image` -> `/recipes/create/image`
  * `/groups/webhooks` -> `/households/webhooks`
  * `/groups/shopping/items` -> `/households/shopping/items`
  * `/groups/shopping/lists` -> `/households/shopping/lists`
  * `/groups/mealplans` -> `/households/mealplans`
  * `/groups/mealplans/rules` -> `/households/mealplans/rules`
  * `/groups/invitations` -> `/households/invitations`
  * `/groups/recipe-actions` -> `/households/recipe-actions`
  * `/groups/events/notifications` -> `/households/events/notifications`
  * `/groups/cookbooks` -> `/households/cookbooks`
  * `/explore/foods/{group_slug}` -> `/explore/groups/{group_slug}/foods`
  * `/explore/organizers/{group_slug}/categories` -> `/explore/groups/{group_slug}/categories`
  * `/explore/organizers/{group_slug}/tags` -> `/explore/groups/{group_slug}/tags`
  * `/explore/organizers/{group_slug}/tools` -> `/explore/groups/{group_slug}/tools`
  * `/explore/cookbooks/{group_slug}` -> `/explore/groups/{group_slug}/cookbooks`
  * `/explore/recipes/{group_slug}` -> `/explore/groups/{group_slug}/recipes`


`/groups/members` previously returned a `UserOut` object, but now returns a `UserSummary`. Should you need the full user information (username, email, etc.), rather than just the summary, see `/households/members` instead for the household members. `/groups/members` previously returned a list of users, but now returns paginated users (similar to all other list endpoints).
These endpoints have been completely removed:
  * `/admin/analytics` (no longer used)
  * `/groups/permissions` (see household permissions)
  * `/groups/statistics` (see household statistics)
  * `/groups/categories` (see organizer endpoints)
  * `/recipes/summary/untagged` (no longer used)
  * `/recipes/summary/uncategorized` (no longer used)
  * `/users/group-users` (see `/groups/members` and `/households/members`)


### Frontend Links
These frontend pages have moved:
  * `/group/mealplan/...` -> `/household/mealplan/...`
  * `/group/members` -> `/household/members`
  * `/group/notifiers` -> `/household/notifiers`
  * `/group/webhooks` -> `/household/webhooks`


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
