[ Skip to content ](https://docs.mealie.io/contributors/developers-guide/building-packages/#building-packages)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Building Packages
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
      * Building Packages  [ Building Packages  ](https://docs.mealie.io/contributors/developers-guide/building-packages/)
        * [ Python packages  ](https://docs.mealie.io/contributors/developers-guide/building-packages/#python-packages)
        * [ Docker image  ](https://docs.mealie.io/contributors/developers-guide/building-packages/#docker-image)
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


  * [ Python packages  ](https://docs.mealie.io/contributors/developers-guide/building-packages/#python-packages)
  * [ Docker image  ](https://docs.mealie.io/contributors/developers-guide/building-packages/#docker-image)


# Building Packages
Released packages are [built and published via GitHub actions](https://docs.mealie.io/contributors/developers-guide/maintainers/#drafting-releases).
## Python packages
To build Python packages locally for testing, use [`task`](https://docs.mealie.io/contributors/developers-guide/starting-dev-server/#without-dev-containers). After installing `task`, run `task py:package` to perform all the steps needed to build the package and a requirements file. To do it manually, run:
```
pushd frontend
yarnpkg install
yarnpkg generate
popd
rm -r mealie/frontend
cp -a frontend/dist mealie/frontend
uv build --out-dir dist
uv export --no-editable --no-emit-project --extra pgsql --format requirements-txt --output-file dist/requirements.txt
MEALIE_VERSION=$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
echo "mealie[pgsql]==${MEALIE_VERSION} \\" >> dist/requirements.txt
pip hash dist/mealie-${MEALIE_VERSION}-py3-none-any.whl | tail -n1 | tr -d '\n' >> dist/requirements.txt
echo " \\" >> dist/requirements.txt
pip hash dist/mealie-${MEALIE_VERSION}.tar.gz | tail -n1 >> dist/requirements.txt

```

The Python package can be installed with all of its dependencies pinned to the versions tested by the developers with:
```
pip3 install -r dist/requirements.txt --find-links dist

```

To install with the latest but still compatible dependency versions, instead run `pip3 install dist/mealie-$VERSION-py3-none-any.whl` (where `$VERSION` is the version of mealie to install).
## Docker image
One way to build the Docker image is to run the following command in the project root directory:
```
docker build --tag mealie:dev --file docker/Dockerfile --build-arg COMMIT=$(git rev-parse HEAD) .

```

The Docker image can be built from the pre-built Python packages with the task command `task docker:build-from-package`. This is equivalent to:
```
docker build --tag mealie:dev --file docker/Dockerfile --build-arg COMMIT=$(git rev-parse HEAD) --build-context packages=dist .

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
