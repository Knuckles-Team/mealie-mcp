[ Skip to content ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/#bash)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Bulk Url Import
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
      * Bulk Url Import  [ Bulk Url Import  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/)
        * [ Bash  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/#bash)
        * [ Go  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/#go)
        * [ Python  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/#python)
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


  * [ Bash  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/#bash)
  * [ Go  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/#go)
  * [ Python  ](https://docs.mealie.io/documentation/community-guide/bulk-url-import/#python)


# Bulk Url Import
Info
This guide was submitted by a community member. Find something wrong? Submit a PR to get it fixed!
Recipes can be imported in bulk from a file containing a list of URLs. This can be done using the following bash or python scripts with the `list` file containing one URL per line.
#### Bash
```
#!/bin/bash

function authentication () {
  auth=$(curl -X 'POST' \
    "$3/api/auth/token" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=&username='$1'&password='$2'&scope=&client_id=&client_secret=')

    echo $auth |  sed -e 's/.*token":"\(.*\)",.*/\1/'
}

function import_from_file () {
  while IFS= read -r line
  do
    echo $line
    curl -X 'POST' \
      "$3/api/recipes/create/url" \
      -H "Authorization: Bearer $2" \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{"url": "'$line'" }'
    echo
  done < "$1"
}

input="list"
mail="changeme@example.com"
password="MyPassword"
mealie_url=http://localhost:9000


token=$(authentication $mail $password $mealie_url)
import_from_file $input $token $mealie_url

```

#### Go
See [Jleagle/mealie-importer](https://github.com/Jleagle/mealie-importer).
#### Python
```
import requests
import re

def authentication(mail, password, mealie_url):
  headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  data = {
    'grant_type': '',
    'username': mail,
    'password': password,
    'scope': '',
    'client_id': '',
    'client_secret': ''
  }
  auth = requests.post(mealie_url + "/api/auth/token", headers=headers, data=data)
  token = re.sub(r'.*token":"(.*)",.*', r'\1', auth.text)
  return token

def import_from_file(input_file, token, mealie_url):
  with open(input_file) as fp:
    for l in fp:
      line = re.sub(r'(.*)\n', r'\1', l)
      print(line)
      headers = {
        'Authorization': "Bearer " + token,
        'accept': 'application/json',
        'Content-Type': 'application/json'
      }
      data = {
        'url': line
      }
      response = requests.post(mealie_url + "/api/recipes/create/url", headers=headers, json=data)
      print(response.text)

input_file="list"
mail="changeme@example.com"
password="MyPassword"
mealie_url="http://localhost:9000"


token = authentication(mail, password, mealie_url)
import_from_file(input_file, token, mealie_url)

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
