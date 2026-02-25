[ Skip to content ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#migrating-to-mealie-v1-release)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Version 1 Migration
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
    * Version 1 Migration  [ Version 1 Migration  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/)
      * [ Migration Considerations  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#migration-considerations)
      * [ Step 1: Setting Up The New Application  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-1-setting-up-the-new-application)
      * [ Step 2: Exporting Your Data from Pre-v1  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-2-exporting-your-data-from-pre-v1)
      * [ Step 3: Using the Migration Tool  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-3-using-the-migration-tool)
      * [ Step 4: Reviewing New Features  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-4-reviewing-new-features)
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


  * [ Migration Considerations  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#migration-considerations)
  * [ Step 1: Setting Up The New Application  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-1-setting-up-the-new-application)
  * [ Step 2: Exporting Your Data from Pre-v1  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-2-exporting-your-data-from-pre-v1)
  * [ Step 3: Using the Migration Tool  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-3-using-the-migration-tool)
  * [ Step 4: Reviewing New Features  ](https://docs.mealie.io/documentation/getting-started/migrating-to-mealie-v1/#step-4-reviewing-new-features)


# Migrating to Mealie v1 Release
The version 1 release of Mealie should be seen as an entirely different application. A whole host of changes have been made to improve the application, performance, and developer experience. Most of these improvements required significant breaking changes in the application that made a clean and easy migration impossible. However, if you've used Mealie prior to v1, there is a migration path to get most of your data from the old version to the new v1 version.
Currently Supported Migration Data
Supporting more data is a work in progress, but not a current priority. I'm open to PRs to add support for additional data.
  * Recipes
  * Categories
  * Tags
  * Users
  * Groups
  * Meal Plans
  * Cookbooks / Pages


## Migration Considerations
Before you migrate to v1.0.0 please consider the following:
**API Integration Will Break**
Several of the endpoints in the API have changed. This means that you will need to update your code to use the new endpoints.
**Recipes Are Private By Default**
By default, recipes can only be viewed by logged-in users. You can fine-tune public recipe access, or keep your instance fully private. For more information, check out the [Permissions and Public Access guide](https://docs.mealie.io/documentation/getting-started/usage/permissions-and-public-access/).
## Step 1: Setting Up The New Application
Given the nature of the upgrade, it is highly recommended that you stand up a new instance of mealie along side your current instance. This will allow you to migrate your data safely and quickly without any issues. Follow the instructions in the [Installation Checklist](https://docs.mealie.io/documentation/getting-started/installation/installation-checklist/) to get started. Once that's complete and you can login, continue here with step 2.
## Step 2: Exporting Your Data from Pre-v1
In your instance of Mealie prior to v1, perform an export (backup) of your data in the Admin section. Be sure to include the recipes when performing the export. Checking additional items won't impact the migration, but they will be ignored if they are included. The backups section is located on the admin dashboard in the section labeled "Backups":
![pre-v1-backup-location-image](https://docs.mealie.io/assets/img/pre-v1-backup-location.png)
## Step 3: Using the Migration Tool
In your new v1 instance, navigate to `/group/migrations` and select "Mealie" from the dropdown selector. Upload the exported data from your pre-v1 instance. Optionally, you can tag all the recipes you've imported with the `mealie_alpha` tag to help you identify them. Once the upload has finished, submit the form and your migration will begin. This may take some time, but when it's complete you'll be provided a new entry in the "Previous Migrations" table below. Be sure to review the migration report to make sure everything was successful. There may be instances where some of the recipes were not imported, but the migration will still import all the successful recipes.
In most cases, it's faster to manually migrate the recipes that didn't take instead of trying to identify why the recipes failed to import. If you're experiencing issues with the migration tool, please open an issue on GitHub.
Recipe Owners
When perform any migration, it will automatically assign the owner of the recipe to the user that performed the migration. All group members will still be able to access the recipe; however, the owner has special permissions to lock the recipe from edits from other users.
## Step 4: Reviewing New Features
v1 Comes with a whole host of new features and improvements. Check out the changelog to get a sense for what's new.
  * [Github releases changelog](https://github.com/mealie-recipes/mealie/releases)


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
