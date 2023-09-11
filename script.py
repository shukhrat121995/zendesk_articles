import requests

# Set up the source and target API tokens and subdomains
source_subdomain = "provet-support"
target_subdomain = "provetsupport1615548161"

def check_translations(production_id, cloud_sb_id):
    languages = [
        "sv-se",
        "nb-no",
        "et-ee",
        "es-es",
        "da-dk",
    ]
    for language in languages:
        source_article_endpoint = f"https://{source_subdomain}.zendesk.com/api/v2/help_center/articles/{production_id}/translations/{language}"
        target_article_endpoint = f"https://{target_subdomain}.zendesk.com/api/v2/help_center/articles/{cloud_sb_id}/translations.json"

        # Check production article
        response = requests.get(source_article_endpoint)
        if response.status_code == 200:
            translation = response.json()["translation"]
            del translation["id"]
            del translation["url"]
            del translation["html_url"]
            del translation["source_id"]
            del translation["source_type"]
            del translation["created_at"]
            del translation["updated_at"]
            del translation["updated_by_id"]
            del translation["created_by_id"]

            # Create payload
            payload = {"translation": translation}
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST",
                target_article_endpoint,
                auth=('<email>/token', '<token>'),
                headers=headers,
                json=payload
            )
            if response.status_code == 201:
                print(f"SUCCESS! Translation for an article with an ID:{production_article_id} created in {target_subdomain}.")
            else:
                print(f"ERROR! Error creating translation")
        else:
            print(f"Article with an ID:({production_id}) is not translated to {language}")



for page in range(1, 4):
    # Set up the API endpoints
    source_articles_endpoint = f"https://{source_subdomain}.zendesk.com/api/v2/help_center/en-gb/articles.json?page={page}&per_page=100"
    target_articles_endpoint = f"https://{target_subdomain}.zendesk.com/api/v2/help_center/en-gb/sections/10022449010973/articles"

    # Retrieve the articles from the source account
    response = requests.get(source_articles_endpoint)
    response.raise_for_status()
    articles = response.json()["articles"]

    # Loop through the articles and create them in the target account
    for article in articles:
        # Set up the request body for the new article
        production_article_id = article['id']
        del article["id"]
        del article["url"]
        del article["html_url"]
        article["permission_group_id"] = 2515558
        article["locale"] = "en-gb"
        article["user_segment_id"] = None
        article["author_id"] = None
        
        # Create payload
        payload = {"article": article, "notify_subscribers": False}
        headers = {
            "Content-Type": "application/json",
        }

        # Make the API request to create the article in the target account
        response = requests.request(
            "POST",
            target_articles_endpoint,
            auth=('<email>/token', '<token>'),
            headers=headers,
            json=payload
        )
        if response.status_code == 201:
            print(f"Article {article['title']} created in {target_subdomain}.")
            cloud_sb_article_id = response.json()['article']['id']
            check_translations(production_article_id, cloud_sb_article_id)
        else:
            print(f"Error creating article {article['title']} in {target_subdomain}: {response.status_code}")
