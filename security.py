
import os
import base64
import hmac
import hashlib

from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# Carrega as configurações do arquivo .env
load_dotenv()


# Configuração inicial do Argon2id
password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)



def obter_chave():
    """
    Obtém e valida a chave AES-256 armazenada no ambiente.
    """

    chave_texto = os.getenv("FLOWTECH_ENCRYPTION_KEY")

    if not chave_texto:
        raise RuntimeError(
            "A chave FLOWTECH_ENCRYPTION_KEY não foi encontrada."
        )

    try:
        # Remove espaços acidentais e completa o padding Base64.
        chave_texto = chave_texto.strip()
        chave_texto += "=" * (-len(chave_texto) % 4)

        chave = base64.b64decode(
            chave_texto,
            altchars=b"-_",
            validate=True
        )

    except Exception as erro:
        raise RuntimeError(
            "A chave de criptografia possui formato inválido."
        ) from erro

    if len(chave) != 32:
        raise RuntimeError(
            "A chave AES-256 precisa possuir exatamente 32 bytes."
        )

    return chave


def gerar_hash_senha(senha):
    """
    Gera um hash Argon2id para armazenar no banco de dados.
    """

    if not isinstance(senha, str) or not senha:
        raise ValueError("A senha não pode estar vazia.")

    return password_hasher.hash(senha)


def verificar_senha(senha_digitada, senha_armazenada):
    """
    Verifica a senha.
    Retorna:
    (senha_correta, precisa_atualizar_hash)

    A comparação com texto puro é temporária, para permitir
    a migração gradual das senhas antigas.
    """

    if not senha_digitada or not senha_armazenada:
        return False, False

    if senha_armazenada.startswith("$argon2"):
        try:
            senha_correta = password_hasher.verify(
                senha_armazenada,
                senha_digitada
            )

            precisa_atualizar = (
                password_hasher.check_needs_rehash(
                    senha_armazenada
                )
            )

            return senha_correta, precisa_atualizar

        except (
            VerifyMismatchError,
            VerificationError,
            InvalidHashError
        ):
            return False, False

    # Compatibilidade temporária com senhas antigas em texto puro.
    senha_correta = hmac.compare_digest(
        senha_digitada,
        senha_armazenada
    )

    return senha_correta, senha_correta


def criptografar_dado(valor, contexto):
    """
    Criptografa um dado utilizando AES-256-GCM.
    O contexto vincula o conteúdo à finalidade informada.
    """

    if valor is None:
        return None

    chave = obter_chave()

    valor_bytes = str(valor).encode("utf-8")
    contexto_bytes = contexto.encode("utf-8")

    nonce = os.urandom(12)

    aes = AESGCM(chave)

    criptografado = aes.encrypt(
        nonce,
        valor_bytes,
        contexto_bytes
    )

    resultado = nonce + criptografado

    resultado_base64 = base64.urlsafe_b64encode(
        resultado
    ).decode("utf-8")

    return "enc:v1:" + resultado_base64


def descriptografar_dado(valor, contexto):
    """
    Descriptografa um dado protegido por AES-256-GCM.
    """

    if valor is None:
        return None

    if not valor.startswith("enc:v1:"):
        raise ValueError(
            "O dado não possui o formato de criptografia esperado."
        )

    chave = obter_chave()

    conteudo = base64.urlsafe_b64decode(
        valor[7:]
    )

    nonce = conteudo[:12]
    criptografado = conteudo[12:]

    aes = AESGCM(chave)

    valor_original = aes.decrypt(
        nonce,
        criptografado,
        contexto.encode("utf-8")
    )

    return valor_original.decode("utf-8")


def gerar_indice_pesquisa(valor, chave_indice):
    """
    Gera um índice HMAC-SHA256 para pesquisas exatas.
    A chave de índice deve ser diferente da chave AES.
    """

    if valor is None:
        return None

    valor_normalizado = str(valor).strip().casefold()

    resultado = hmac.new(
        chave_indice.encode("utf-8"),
        valor_normalizado.encode("utf-8"),
        hashlib.sha256
    )

    return resultado.hexdigest()
