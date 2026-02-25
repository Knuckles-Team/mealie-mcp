[ Skip to content ](https://docs.mealie.io/documentation/getting-started/installation/sqlite/#installing-with-sqlite)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
SQLite (Recommended)
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
      * [ Migration Guide  ](https://docs.mealie.io/contributors/developers-guide/migration-guide/)
    * Guides
      * [ Improving Ingredient Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/)
  * News
    * Surveys
      * [ October 2024  ](https://docs.mealie.io/news/surveys/2024-october/overview/)


# Installing with SQLite
Warning
If you're planning on deploying and using Network Attached Storage with Mealie, you should use [Postgres](https://docs.mealie.io/documentation/getting-started/installation/postgres/) instead of SQLite. SQLite is not designed to be used with Network Attached Storage and can cause data corruption, or locked database errors
SQLite is a popular, open source, self-contained, zero-configuration database that is the ideal choice for Mealie when you have 1-20 Users. Below is a ready to use docker-compose.yaml file for deploying Mealie on your server.
**For Environment Variable Configuration, see** [Backend Configuration](https://docs.mealie.io/documentation/getting-started/installation/backend-config/)
```
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:v3.11.0 # [](https://docs.mealie.io/documentation/getting-started/installation/sqlite/#__code_0_annotation_3)
    container_name: mealie
    restart: always
    ports:
        - "9925:9000" # [](https://docs.mealie.io/documentation/getting-started/installation/sqlite/#__code_0_annotation_1)
    deploy:
      resources:
        limits:
          memory: 1000M # [](https://docs.mealie.io/documentation/getting-started/installation/sqlite/#__code_0_annotation_2)
    volumes:
      - mealie-data:/app/data/
    environment:
      # Set Backend ENV Variables Here
      ALLOW_SIGNUP: "false"
      PUID: 1000
      PGID: 1000
      TZ: America/Anchorage
      BASE_URL: https://mealie.yourdomain.com

volumes:
  mealie-data:

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
