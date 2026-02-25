[ Skip to content ](https://docs.mealie.io/documentation/getting-started/updating/#updating-mealie)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Updating
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
    * Updating  [ Updating  ](https://docs.mealie.io/documentation/getting-started/updating/)
      * [ Before Upgrading  ](https://docs.mealie.io/documentation/getting-started/updating/#before-upgrading)
      * [ Options  ](https://docs.mealie.io/documentation/getting-started/updating/#options)
      * [ Example  ](https://docs.mealie.io/documentation/getting-started/updating/#example)
      * [ Upgrading to Mealie v1 or later  ](https://docs.mealie.io/documentation/getting-started/updating/#upgrading-to-mealie-v1-or-later)
      * [ Backing Up Your Data  ](https://docs.mealie.io/documentation/getting-started/updating/#backing-up-your-data)
      * [ Docker  ](https://docs.mealie.io/documentation/getting-started/updating/#docker)
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
      * [ Migration Guide  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/)
    * Guides
      * [ Improving Ingredient Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/)
  * News
    * Surveys
      * [ October 2024  ](https://docs.mealie.io/news/surveys/2024-october/overview/)


  * [ Before Upgrading  ](https://docs.mealie.io/documentation/getting-started/updating/#before-upgrading)
  * [ Options  ](https://docs.mealie.io/documentation/getting-started/updating/#options)
  * [ Example  ](https://docs.mealie.io/documentation/getting-started/updating/#example)
  * [ Upgrading to Mealie v1 or later  ](https://docs.mealie.io/documentation/getting-started/updating/#upgrading-to-mealie-v1-or-later)
  * [ Backing Up Your Data  ](https://docs.mealie.io/documentation/getting-started/updating/#backing-up-your-data)
  * [ Docker  ](https://docs.mealie.io/documentation/getting-started/updating/#docker)


# Updating Mealie
Read The Release Notes
You MUST read the release notes prior to upgrading your container. Mealie has a robust backup and restore system for managing your data. Pre-v1.0.0 versions of Mealie use a different database structure, so if you are upgrading from pre-v1.0.0 to v1.0.0, you MUST backup your data and then re-import it. Even if you are already on v1.0.0, it is strongly recommended to backup all data before updating.
### Before Upgrading
  * [Read The Release Notes](https://github.com/mealie-recipes/mealie/releases)
  * Identify Breaking Changes
  * Create a Backup and Download from the UI
  * Upgrade


Improved Image Processing
Starting with
```
docker exec -it mealie bash
python /opt/mealie/lib64/python3.12/site-packages/mealie/scripts/reprocess_images.py

```

### Options
  * `--workers N`: Number of worker threads (default: 2, safe for low-powered devices)
  * `--force-all`: Reprocess all recipes regardless of current image state


### Example
```
python /opt/mealie/lib64/python3.12/site-packages/mealie/scripts/reprocess_images.py --workers 8

```

## Upgrading to Mealie v1 or later
If you are upgrading from pre-v1.0.0 to v1.0.0 or later (v2.0.0, etc.), make sure you read [Migrating to Mealie v1](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/)!
## Backing Up Your Data
[See Backups and Restore Section](https://docs.mealie.io/documentation/getting-started/usage/backups-and-restoring/) for details on backing up your data
## Docker
For all setups using Docker, the updating process looks something like this:
  * Stop the container using `docker compose down`
  * If you are not using the latest tag, change the version (image tag) in your docker-compose file
  * Pull the latest image using `docker compose pull`
  * Start the container again using `docker compose up -d`


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
