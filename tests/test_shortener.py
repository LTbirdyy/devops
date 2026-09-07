from app.shortener import generate_short_code, ALPHABET


def test_generate_short_code_has_correct_length():
    code = generate_short_code(length=6)
    assert len(code) == 6


def test_generate_short_code_uses_only_valid_characters():
    code = generate_short_code(length=20)
    assert all(char in ALPHABET for char in code)


def test_generate_short_code_is_random():
    # Gerar várias vezes deve, com altíssima probabilidade, produzir códigos diferentes
    codes = {generate_short_code() for _ in range(50)}
    assert len(codes) > 1
