from scraper import fetch_article

paras = fetch_article()
for i, p in enumerate(paras[:3]):
    print(f"{i}: {p[:120]}")
