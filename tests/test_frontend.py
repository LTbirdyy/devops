def test_homepage_serves_html_and_form(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # Valida apenas tags semânticas essenciais, sem depender de textos ou classes
    html = response.text
    assert "<form" in html
    assert 'type="url"' in html
    assert 'type="submit"' in html
