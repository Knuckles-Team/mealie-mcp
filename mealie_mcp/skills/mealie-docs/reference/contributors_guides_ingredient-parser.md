[ Skip to content ](https://docs.mealie.io/contributors/guides/ingredient-parser/#improving-the-ingredient-parser)
[ Looking for a hosted solution? Explore Recipinned from the creator of Mealie ](https://recipinned.com)
[ ](https://docs.mealie.io/ "Mealie")
Mealie
Improving Ingredient Parser
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
      * Improving Ingredient Parser  [ Improving Ingredient Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/)
        * [ Improving The CRF Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/#improving-the-crf-parser)
        * [ Alternative Parsers  ](https://docs.mealie.io/contributors/guides/ingredient-parser/#alternative-parsers)
        * [ Links  ](https://docs.mealie.io/contributors/guides/ingredient-parser/#links)
  * News
    * Surveys
      * [ October 2024  ](https://docs.mealie.io/news/surveys/2024-october/overview/)


  * [ Improving The CRF Parser  ](https://docs.mealie.io/contributors/guides/ingredient-parser/#improving-the-crf-parser)
  * [ Alternative Parsers  ](https://docs.mealie.io/contributors/guides/ingredient-parser/#alternative-parsers)
  * [ Links  ](https://docs.mealie.io/contributors/guides/ingredient-parser/#links)


# Improving the Ingredient Parser
Mealie uses Conditional Random Fields (CRFs) for parsing and processing ingredients. The model used for ingredients is based off a data set of over 100,000 ingredients from a dataset compiled by the New York Times. I believe that the model used is sufficient enough to handle most of the ingredients, therefore, more data to train the model won't necessarily help improve the model.
## Improving The CRF Parser
To improve results with the model, you'll likely need to focus on improving the tokenization and parsing of the original string to aid the model in determine what the ingredient is. Data science is not my forte, but I have done some tokenization to improve the model. You can find that code under `/mealie/services/parser_services/crfpp` along with some other utility functions to aid in the tokenization and processing of ingredient strings.
The best way to test on improving the parser is to register additional test cases in `/mealie/tests/unit_tests/test_crfpp_parser.py` and run the test after making changes to the tokenizer. Note that the test cases DO NOT run in the CI environment, therefore you will need to have CRF++ installed on your machine. If you're using a Mac the easiest way to do this is through brew.
When submitting a PR to improve the parser it is important to provide your test cases, the problem you were trying to solve, and the results of the changes you made. As the tests don't run in CI, not providing these details may delay your PR from being merged.
## Alternative Parsers
Alternatively, you can register a new parser by fulfilling the `ABCIngredientParser` interface. Satisfying this single method interface allows us to register additional parsing strategies at runtime and gives the user several options when trying to parse a recipe.
## Links
  * [Pretrained Model](https://github.com/mealie-recipes/mealie-nlp-model)
  * [CRF++ (Forked)](https://github.com/hay-kot/crfpp)


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
