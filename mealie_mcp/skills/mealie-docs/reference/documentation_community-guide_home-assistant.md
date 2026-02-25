[ Skip to content ](https://docs.mealie.io/documentation/community-guide/home-assistant/#display-todays-meal-in-lovelace)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Home Assistant
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
      * Home Assistant  [ Home Assistant  ](https://docs.mealie.io/documentation/community-guide/home-assistant/)
        * [ Display Today's Meal in Lovelace  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#display-todays-meal-in-lovelace)
        * [ Steps:  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#steps)
          * [ 1. Get your API Token  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#1-get-your-api-token)
          * [ 2. Create Home Assistant Sensors  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#2-create-home-assistant-sensors)
          * [ 3. Create a Camera Entity  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#3-create-a-camera-entity)
          * [ 4. Create a Lovelace Card  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#4-create-a-lovelace-card)
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


  * [ Display Today's Meal in Lovelace  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#display-todays-meal-in-lovelace)
  * [ Steps:  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#steps)
    * [ 1. Get your API Token  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#1-get-your-api-token)
    * [ 2. Create Home Assistant Sensors  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#2-create-home-assistant-sensors)
    * [ 3. Create a Camera Entity  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#3-create-a-camera-entity)
    * [ 4. Create a Lovelace Card  ](https://docs.mealie.io/documentation/community-guide/home-assistant/#4-create-a-lovelace-card)


# Home Assistant
Info
This guide was submitted by a community member. Find something wrong? Submit a PR to get it fixed!
In a lot of ways, Home Assistant is why this project exists! Since Mealie has a robust API it makes it a great fit for interacting with Home Assistant and pulling information into your dashboard.
## Display Today's Meal in Lovelace
You can use the Mealie API to get access to meal plans in Home Assistant like in the image below.
![api-extras-gif](https://docs.mealie.io/assets/img/home-assistant-card.png)
## Steps:
### 1. Get your API Token
Create an API token from Mealie's User Settings page (see [this page](https://docs.mealie.io/documentation/getting-started/api-usage/#getting-a-token) to learn how).
### 2. Create Home Assistant Sensors
Create REST sensors in home assistant to get the details of today's meal. We will create sensors to get the name and ID of the first meal in today's meal plan (note that this may not be what is wanted if there is more than one meal planned for the day). We need the ID as well as the name to be able to retrieve the image for the meal.
Make sure the url and port (`http://mealie:9000`) matches your installation's address and _API_ port.
```
rest:
  - resource: "http://mealie:9000/api/households/mealplans/today"
    method: GET
    headers:
      Authorization: Bearer <<API_TOKEN>>
    scan_interval: 3600
    sensor:
      - name: Mealie todays meal
        value_template: "{{ value_json[0]['recipe']['name'] }}"
        force_update: true
        unique_id: mealie_todays_meal
      - name: Mealie todays meal ID
        value_template: "{{ value_json[0]['recipe']['id'] }}"
        force_update: true
        unique_id: mealie_todays_meal_id

```

### 3. Create a Camera Entity
We will create a camera entity to display the image of today's meal in Lovelace.
In Home Assistant's `Integrations` page, create a new `generic camera` entity.
In the still image url field put in: `http://mealie:9000/api/media/recipes/{{states('sensor.mealie_todays_meal_id')}}/images/min-original.webp`
Under the entity page for the new camera, rename it. e.g. `camera.mealie_todays_meal_image`
### 4. Create a Lovelace Card
Create a picture entity card and set the entity to `mealie_todays_meal` and the camera entity to `camera.mealie_todays_meal_image` or set in the yaml directly.
```
show_state: true
show_name: true
camera_view: auto
type: picture-entity
entity: sensor.mealie_todays_meal
name: Dinner Tonight
camera_image: camera.mealie_todays_meal_image
card_mod:
  style: |
    ha-card {
    max-height: 300px !important;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    }

```

Tip
Due to how Home Assistant works with images, I had to include the additional styling to get the images to not appear distorted. This requires an [additional installation](https://github.com/thomasloven/lovelace-card-mod) from HACS.
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
