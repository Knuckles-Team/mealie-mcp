[ Skip to content ](https://docs.mealie.io/documentation/community-guide/swag/#using-swag-as-reverse-proxy)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Reverse Proxy (SWAG)
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
      * Reverse Proxy (SWAG)  [ Reverse Proxy (SWAG)  ](https://docs.mealie.io/documentation/community-guide/swag/)
        * [ Step 1: Get a domain  ](https://docs.mealie.io/documentation/community-guide/swag/#step-1-get-a-domain)
        * [ Step 2: Set-up SWAG  ](https://docs.mealie.io/documentation/community-guide/swag/#step-2-set-up-swag)
        * [ Step 3: Change the config files  ](https://docs.mealie.io/documentation/community-guide/swag/#step-3-change-the-config-files)
        * [ Step 4: Port-forward port 443  ](https://docs.mealie.io/documentation/community-guide/swag/#step-4-port-forward-port-443)
        * [ Step 5: Restart SWAG  ](https://docs.mealie.io/documentation/community-guide/swag/#step-5-restart-swag)
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


  * [ Step 1: Get a domain  ](https://docs.mealie.io/documentation/community-guide/swag/#step-1-get-a-domain)
  * [ Step 2: Set-up SWAG  ](https://docs.mealie.io/documentation/community-guide/swag/#step-2-set-up-swag)
  * [ Step 3: Change the config files  ](https://docs.mealie.io/documentation/community-guide/swag/#step-3-change-the-config-files)
  * [ Step 4: Port-forward port 443  ](https://docs.mealie.io/documentation/community-guide/swag/#step-4-port-forward-port-443)
  * [ Step 5: Restart SWAG  ](https://docs.mealie.io/documentation/community-guide/swag/#step-5-restart-swag)


# Using SWAG as Reverse Proxy
Info
This guide was submitted by a community member. Find something wrong? Submit a PR to get it fixed!
To make the setup of a Reverse Proxy much easier, Linuxserver.io developed [SWAG](https://github.com/linuxserver/docker-swag).
SWAG - Secure Web Application Gateway (formerly known as letsencrypt, no relation to Let's Encrypt™) sets up an Nginx web server and reverse proxy with PHP support and a built-in certbot client that automates free SSL server certificate generation and renewal processes (Let's Encrypt and ZeroSSL). It also contains fail2ban for intrusion prevention.
## Step 1: Get a domain
The first step is to grab a dynamic DNS if you don't have your own subdomain already. You can get this from for example [DuckDNS](https://www.duckdns.org).
## Step 2: Set-up SWAG
Then you will need to set up SWAG, the variables of the docker-compose.yaml file are explained on the Github page of [SWAG](https://github.com/linuxserver/docker-swag). This is an example of how to set it up using duckdns and docker compose.
docker-compose.yaml
```
version: "3.1"
services:
  swag:
    image: ghcr.io/linuxserver/swag
    container_name: swag
    cap_add:
      - NET_ADMIN
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Brussels
      - URL=<mydomain.duckdns>
      - SUBDOMAINS=wildcard
      - VALIDATION=duckdns
      - CERTPROVIDER= #optional
      - DNSPLUGIN= #optional
      - DUCKDNSTOKEN=<duckdnstoken>
      - EMAIL=<e-mail> #optional
      - ONLY_SUBDOMAINS=false #optional
      - EXTRA_DOMAINS=<extradomains> #optional
      - STAGING=false #optional
    volumes:
      - /etc/config/swag:/config
    ports:
      - 443:443
      - 80:80 #optional
    restart: unless-stopped

```

Don't forget to change the `mydomain.duckdns` into your personal domain and the `duckdnstoken` into your token and remove the brackets.
## Step 3: Change the config files
Navigate to the config folder of SWAG and head to `proxy-confs`. If you used the example above, you should navigate to: `/etc/config/swag/nginx/proxy-confs/`. There are a lot of preconfigured files to use for different apps such as radarr, sonarr, overseerr, ...
To use the bundled configuration file, simply rename `mealie.subdomain.conf.sample` in the proxy-confs folder to `mealie.subdomain.conf`. Currently, you will have to change the $upstream_app and $upstream_port to mealie-frontend and port 3000. This will be added to the bundled config files once the beta is released. Alternatively, you can create a new file `mealie.subdomain.conf` in proxy-confs with the following configuration:
mealie.subdomain.conf
```
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  server_name mealie.*;

  include /config/nginx/ssl.conf;

  client_max_body_size 0;

  location / {
    include /config/nginx/proxy.conf;
    include /config/nginx/resolver.conf;
    set $upstream_app mealie-frontend;
    set $upstream_port 3000;
    set $upstream_proto http;
    proxy_pass $upstream_proto://$upstream_app:$upstream_port;
  }
}

```

## Step 4: Port-forward port 443
Since SWAG allows you to set up a secure connection, you will need to open port 443 on your router for encrypted traffic. Port 80 can be used as well if you want to have the http to https redirect working. This is however optional and not recommended, only if you have a specific usage for it.
## Step 5: Restart SWAG
When you change anything in the config of Nginx, you will need to restart the container using `docker restart swag`. If everything went well, you can now access mealie on the subdomain you configured: mealie.mydomain.duckdns.org
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
