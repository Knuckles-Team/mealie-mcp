[ Skip to content ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/#javascript-can-only-be-run-via-shortcuts-on-the-safari-browser-on-macos-and-ios-if-you-do-not-use-safari-you-may-skip-this-section)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
iOS Shortcut
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
      * iOS Shortcut  [ iOS Shortcut  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/)
        * [ Javascript can only be run via Shortcuts on the Safari browser on MacOS and iOS. If you do not use Safari you may skip this section  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/#javascript-can-only-be-run-via-shortcuts-on-the-safari-browser-on-macos-and-ios-if-you-do-not-use-safari-you-may-skip-this-section)
        * [ Initial Setup  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/#initial-setup)
        * [ Using the Shortcut  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/#using-the-shortcut)
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


  * [ Javascript can only be run via Shortcuts on the Safari browser on MacOS and iOS. If you do not use Safari you may skip this section  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/#javascript-can-only-be-run-via-shortcuts-on-the-safari-browser-on-macos-and-ios-if-you-do-not-use-safari-you-may-skip-this-section)
  * [ Initial Setup  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/#initial-setup)
  * [ Using the Shortcut  ](https://docs.mealie.io/documentation/community-guide/ios-shortcut/#using-the-shortcut)


# iOS Shortcut
Info
This guide was submitted by a community member. Find something wrong? Submit a PR to get it fixed!
An easy way to add recipes to Mealie from an Apple device is via an Apple Shortcut. This is a short guide to install an configure a shortcut able to add recipes via a link or image(s).
Note
If adding via images make sure to enable [Mealie's OpenAI Integration](https://docs.mealie.io/documentation/getting-started/installation/open-ai/)
## Javascript can only be run via Shortcuts on the Safari browser on MacOS and iOS. If you do not use Safari you may skip this section
Some sites have begun blocking AI scraping bots, inadvertently blocking the recipe scraping library Mealie uses as well. To circumvent this, the shortcut uses javascript to capture the raw html loaded in the browser and sends that to mealie when possible.
**iOS**
Settings app -> apps -> Shortcuts -> Advanced -> Allow Running Scripts
**MacOS**
Shortcuts app -> Settings (CMD ,) -> Advanced -> Allow Running Scripts
## Initial Setup
An API key is needed to authenticate with mealie. To create an api key for a user, navigate to http://YOUR_MEALIE_URL/user/profile/api-tokens. Alternatively you can create a key via the mealie home page by clicking the user's profile pic in the top left -> Api Tokens
The shortcut can be installed via **[This link](https://www.icloud.com/shortcuts/52834724050b42aebe0f2efd8d067360)**. Upon install, replace "MEALIE_API_KEY" with the API key generated previously and "MEALIE_URI" with the full URL used to access your mealie instance e.g. "http://10.0.0.5:9000" or "https://mealie.domain.com".
## Using the Shortcut
Once installed, the shortcut will automatically appear as an option when sharing an image or webpage. It can also be useful to add the shortcut to the home screen of your device. If selected from the home screen or shortcuts app, a menu will appear with prompts to import via **taking photo(s)** , **selecting photo(s)** , **scanning a URL** , or **pasting a URL**.
Note
Despite the Mealie API being able to accept multiple recipe images for import it is currently impossible to send multiple files in 1 web request via Shortcuts. Instead, the shortcut combines the images into a singular, vertically-concatenated image to send to mealie. This can result in slightly less-accurate text recognition.
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
