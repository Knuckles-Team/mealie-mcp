[ Skip to content ](https://docs.mealie.io/documentation/getting-started/introduction/#about-the-project)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Introduction
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
    * Introduction  [ Introduction  ](https://docs.mealie.io/documentation/getting-started/introduction/)
      * [ Key Features  ](https://docs.mealie.io/documentation/getting-started/introduction/#key-features)
      * [ FAQ  ](https://docs.mealie.io/documentation/getting-started/introduction/#faq)
      * [ Built With  ](https://docs.mealie.io/documentation/getting-started/introduction/#built-with)
      * [ Contributing  ](https://docs.mealie.io/documentation/getting-started/introduction/#contributing)
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


  * [ Key Features  ](https://docs.mealie.io/documentation/getting-started/introduction/#key-features)
  * [ FAQ  ](https://docs.mealie.io/documentation/getting-started/introduction/#faq)
  * [ Built With  ](https://docs.mealie.io/documentation/getting-started/introduction/#built-with)
  * [ Contributing  ](https://docs.mealie.io/documentation/getting-started/introduction/#contributing)


# About The Project
Mealie is a self hosted recipe manager and meal planner with a RestAPI backend and a reactive frontend application built in Vue for a pleasant user experience for the whole family. Easily add recipes into your database by providing the url and Mealie will automatically import the relevant data or add a family recipe with the UI editor. Mealie also provides an API for interactions from 3rd party applications.
[Remember to join the Discord](https://discord.gg/QuStdQGSGK)
## Key Features
  * 🔍 Smart search, mix & match of "quoted literal searches" and keyword search. Fuzzy search ("is it brocolli or broccoli?") is also available when using a Postgres database.
  * 🏷️ Tag recipes with categories or tags for flexible sorting
  * 🕸 Import recipes from around the web by URL
  * 📱 Progressive Web App
  * 📆 Create Meal Plans
  * 🛒 Generate Shopping Lists
  * 🏠 Separate Users into Households and share Recipes
  * 🐳 Easy setup with Docker
  * 🎨 Customize your interface with color themed layouts
  * 🌍 localized in many languages
  * ➕ Plus tons more!
  * Flexible API
    * Custom key/value pairs for recipes
    * Webhook support
    * Interactive API Documentation thanks to [FastAPI](https://fastapi.tiangolo.com/) and [Swagger](https://petstore.swagger.io/)
  * Raw JSON Recipe Editor
  * Migration from other platforms
    * Chowdown
    * Nextcloud Cookbook
    * Copy Me That
    * Paprika
    * Tandoor Recipes
    * DVO Cook'n X3
  * Random Meal Plan generation
    * Advanced rule configuration to fine tune random recipes


## FAQ
See the [Frequently Asked Questions page](https://docs.mealie.io/documentation/getting-started/faq/)
## Built With
  * [Vue.js](https://vuejs.org/)
  * [Vuetify](https://vuetifyjs.com/en/)
  * [FastAPI](https://fastapi.tiangolo.com/)
  * [Docker](https://www.docker.com/)


## Contributing
Contributions are what make the open source community such an amazing place to learn, develop, and create. Any contributions you make are **greatly appreciated**. See the [Contributors Guide](https://docs.mealie.io/contributors/non-coders/) for help getting started.
If you are not a coder, you can still contribute financially. Financial contributions help me prioritize working on this project over others and help me to know that there is a real demand for project development.
[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-green.png)](https://www.buymeacoffee.com/haykot)
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
