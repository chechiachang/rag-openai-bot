# rag-openai-bot


# Setup secrets

In .env

```
# Langsmith (optional)
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=

# Azure openai
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT_NAME=
AZURE_OPENAI_API_VERSION=

# Telegram
BOT_TOKEN=
#BOT_WHITELIST=

# Slack
SLACK_APP_TOKEN=
SLACK_BOT_TOKEN=
```

# Data

Put data directories in ./data, which is ignored by .gitignore. For example, to get the Kubernetes documentation:

```
cd ..

git clone git@github.com:kubernetes/website.git

cp -r website/content/en/* rag-openai-bot/data/kubernetes-docs
```

# Qdrant

up qdrant

```
docker compose up -d
```

down qdrant and wipe data volume

```
docker compose down -v
```
