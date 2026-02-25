[ Skip to content ](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/#backups-and-restores)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Backup and Restoring
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
      * Backup and Restoring  [ Backup and Restoring  ](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/)
        * [ Restoring from a Backup  ](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/#restoring-from-a-backup)
          * [ Postgres Note  ](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/#postgres-note)
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
      * [ Migration Guide  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/)
    * Guides
      * [ Improving Ingredient Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/)
  * News
    * Surveys
      * [ October 2024  ](https://docs.mealie.io/news/surveys/2024-october/overview/)


  * [ Restoring from a Backup  ](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/#restoring-from-a-backup)
    * [ Postgres Note  ](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/#postgres-note)


# Backups and Restores
Mealie provides an integrated mechanic for doing full installation backups of the database.
Navigate to Settings > Admin Settings > Backups or manually by adding `/admin/backups` to your instance URL.
From this page, you will be able to:
  * See a list of available backups
  * Create a backup
  * Upload a backup
  * Delete a backup (Confirmation Required)
  * Download a backup
  * Perform a restore


Tip
If you're using Mealie with SQLite all your data is stored in the /app/data/ folder in the container. You can easily perform entire site backups by stopping the container, and backing up this folder with your chosen tool. This is the **best** way to backup your data.
## Restoring from a Backup
To restore from a backup it needs to be uploaded to your instance which can be done through the web portal. On the top left of the page you'll see an upload button. Click this button and select the backup file you want to upload and it will be available to import shortly. You can alternatively use one of the backups you see on the screen, if one exists.
Before importing it's critical that you understand the following:
  * This is a destructive action and will delete all data in the database
  * This action cannot be undone
  * If this action is successful you will be logged out and you will need to log back in to complete the restore


Tip
If for some reason the restore does not succeed, you can review the logs of what the issue may be, download the backup .ZIP and edit the contents of database.json to potentially resolve the issue. For example, if you receive an error restoring 'shopping-list' you can edit out the contents of that list while allowing other sections to restore. If you would like any assistance on this, reach out over Discord.
Warning
Prior to beta-v5 using a mis-matched version of the database backup will result in an error that will prevent you from using the instance of Mealie requiring you to remove all data and reinstall. Post beta-v5 performing a mismatched restore will throw an error and alert the user of the issue.
### Postgres Note
Restoring the Database when using Postgres requires Mealie to be configured with a postgres **superuser** account. This is due to our usage of massive deleting of data in the database and temporarily setting roles to perform the restore. To perform a restoration on Postgres you will need to _temporarily_ set the Mealie user to a superuser account.
```
ALTER USER mealie WITH SUPERUSER;

-- Run restore from Mealie

ALTER USER mealie WITH NOSUPERUSER;

```

For more information see [GitHub Issue #1500](https://github.com/mealie-recipes/mealie/issues/1500)
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
