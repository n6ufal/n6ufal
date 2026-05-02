import json

with open('repos.json', 'r') as f:
    repos = json.load(f)

langs = {}
for repo in repos:
    if repo.get('language'):
        langs[repo['language']] = langs.get(repo['language'], 0) + 1

if langs:
    top = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:5]
    langs_str = ', '.join([lang for lang, count in top])
else:
    langs_str = "No language data yet"

print(f"TOP_LANGS={langs_str}")