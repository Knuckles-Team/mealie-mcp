[ Skip to content ](https://docs.mealie.io/documentation/getting-started/installation/logs/#logs)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Logs
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
      * Logs  [ Logs  ](https://docs.mealie.io/documentation/getting-started/installation/logs/)
        * [ Highlights  ](https://docs.mealie.io/documentation/getting-started/installation/logs/#highlights)
        * [ Configuration  ](https://docs.mealie.io/documentation/getting-started/installation/logs/#configuration)
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


  * [ Highlights  ](https://docs.mealie.io/documentation/getting-started/installation/logs/#highlights)
  * [ Configuration  ](https://docs.mealie.io/documentation/getting-started/installation/logs/#configuration)


# Logs
## Highlights
  * Logs are written to `/app/data/mealie.log` by default in the container.
  * Logs are also written to stdout and stderr.
  * You can adjust the log level using the `LOG_LEVEL` environment variable.


## Configuration
Starting in v1.5.0 logging is now highly configurable. Using the `LOG_CONFIG_OVERRIDE` you can provide the application with a custom configuration to log however you'd like. This configuration file is based off the [Python Logging Config](https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig). It can be difficult to understand the configuration at first, so here are some resources to help get started.
  * This [YouTube Video](https://www.youtube.com/watch?v=9L77QExPmI0) for a great walkthrough on the logging file format.
  * Our [Logging Config](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/core/logger/logconf.prod.json).


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
