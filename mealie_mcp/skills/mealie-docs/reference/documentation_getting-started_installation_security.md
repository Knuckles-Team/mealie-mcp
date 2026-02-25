[ Skip to content ](https://docs.mealie.io/documentation/getting-started/installation/security/#security-considerations)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Security
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
      * Security  [ Security  ](https://docs.mealie.io/documentation/getting-started/installation/security/)
        * [ Denial of Service  ](https://docs.mealie.io/documentation/getting-started/installation/security/#denial-of-service)
          * [ Mitigation  ](https://docs.mealie.io/documentation/getting-started/installation/security/#mitigation)
        * [ Server Side Request Forgery  ](https://docs.mealie.io/documentation/getting-started/installation/security/#server-side-request-forgery)
          * [ Mitigation  ](https://docs.mealie.io/documentation/getting-started/installation/security/#mitigation_1)
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


  * [ Denial of Service  ](https://docs.mealie.io/documentation/getting-started/installation/security/#denial-of-service)
    * [ Mitigation  ](https://docs.mealie.io/documentation/getting-started/installation/security/#mitigation)
  * [ Server Side Request Forgery  ](https://docs.mealie.io/documentation/getting-started/installation/security/#server-side-request-forgery)
    * [ Mitigation  ](https://docs.mealie.io/documentation/getting-started/installation/security/#mitigation_1)


# Security Considerations
This page is a collection of security considerations for Mealie. It mostly deals with reported issues and how it's possible to mitigate them. Note that this page is for you to use as a guide for how secure you want to make your deployment. It's important to note that most of these will not apply to you, if you:
  1. Run behind a VPN
  2. Use a strong password
  3. Disable Sign-Ups
  4. Don't host for malicious users


Use your best judgement when deciding what to do.
## Denial of Service
By default, the API is **not** rate limited. This leaves Mealie open to a potential **Denial of Service Attack**. While it's possible to perform a **Denial of Service Attack** on any endpoint, there are a few key endpoints that are more vulnerable than others.
  * `/api/recipes/create/url`
  * `/api/recipes/{id}/image`


These endpoints are used to scrape data based off a user provided URL. It is possible for a malicious user to issue multiple requests to download an arbitrarily large external file (e.g a Debian ISO) and sufficiently saturate a CPU assigned to the container. While we do implement some protections against this by chunking the response, and using a timeout strategy, it's still possible to overload the CPU if an attacker issues multiple requests concurrently.
### Mitigation
If you'd like to mitigate this risk, we suggest that you rate limit the API in general, and apply strict rate limits to these endpoints. You can do this by utilizing a reverse proxy. See the following links to get started:
  * [Traefik](https://doc.traefik.io/traefik/middlewares/http/ratelimit/)
  * [Nginx](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
  * [Caddy](https://caddyserver.com/docs/modules/http.handlers.rate_limit)


## Server Side Request Forgery
  * `/api/recipes/create/url`
  * `/api/recipes/{id}/image`


Given the nature of these APIs it's possible to perform a **Server Side Request Forgery** attack. This is where a malicious user can issue a request to an internal network resource, and potentially exfiltrate data. We _do_ perform some checks to mitigate access to resources within your network but at the end of the day, users of Mealie are allowed to trigger HTTP requests on **your server**.
### Mitigation
If you'd like to mitigate this risk, we suggest that you isolate the container that Mealie is running in to ensure that it's access to internal resources is limited only to what is required. _Note that Mealie does require access to the internet for recipe imports._ You might consider isolating Mealie from your home network entirely and only allowing access to the external internet.
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
