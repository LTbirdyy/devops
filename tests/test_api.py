def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shorten_url_returns_short_code(client):
    response = client.post("/shorten", json={"url": "https://www.example.com/pagina-longa"})
    assert response.status_code == 200

    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://www.example.com/pagina-longa"
    assert data["short_code"] in data["short_url"]


def test_redirect_to_original_url(client):
    create_response = client.post("/shorten", json={"url": "https://www.example.com/outra-pagina"})
    short_code = create_response.json()["short_code"]

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code in (302, 307)
    assert redirect_response.headers["location"] == "https://www.example.com/outra-pagina"


def test_redirect_with_invalid_code_returns_404(client):
    response = client.get("/codigo-que-nao-existe")
    assert response.status_code == 404


def test_shorten_url_rejects_invalid_url(client):
    response = client.post("/shorten", json={"url": "isso-nao-e-uma-url"})
    assert response.status_code == 422
