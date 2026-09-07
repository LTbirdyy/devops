import random
import string

from sqlalchemy.orm import Session

from app.config import settings
from app.models import URL

ALPHABET = string.ascii_letters + string.digits  # a-z, A-Z, 0-9 (base62)


def generate_short_code(length: int = None) -> str:
    """Gera uma string aleatória em base62 para usar como código curto."""
    length = length or settings.SHORT_CODE_LENGTH
    return "".join(random.choices(ALPHABET, k=length))


def create_unique_short_code(db: Session) -> str:
    """
    Gera um código curto e garante que ele não colide com um já existente
    no banco. Tenta algumas vezes antes de desistir (colisão é raríssima
    com 6+ caracteres em base62, mas o código precisa ser robusto).
    """
    for _ in range(5):
        code = generate_short_code()
        exists = db.query(URL).filter(URL.short_code == code).first()
        if not exists:
            return code
    raise RuntimeError("Não foi possível gerar um código curto único.")
