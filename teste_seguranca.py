
from security import (
    gerar_hash_senha,
    verificar_senha,
    criptografar_dado,
    descriptografar_dado
)


print("INICIANDO TESTES DE SEGURANÇA DO FLOWTECH")


# TESTE 1 — Hash de senha
senha = "SenhaTesteFlowTech123!"

hash_senha = gerar_hash_senha(senha)

assert hash_senha.startswith("$argon2id$")
assert verificar_senha(senha, hash_senha)[0] is True
assert verificar_senha("SenhaIncorreta", hash_senha)[0] is False

print("[OK] Hash e verificação Argon2id")


# TESTE 2 — Criptografia
dado_original = "12345678900"

dado_criptografado = criptografar_dado(
    dado_original,
    "funcionario.cpf"
)

assert dado_criptografado != dado_original

print("[OK] Criptografia AES-256-GCM")


# TESTE 3 — Descriptografia
dado_recuperado = descriptografar_dado(
    dado_criptografado,
    "funcionario.cpf"
)

assert dado_recuperado == dado_original

print("[OK] Descriptografia AES-256-GCM")


# TESTE 4 — Contexto incorreto
try:
    descriptografar_dado(
        dado_criptografado,
        "cliente.cnpj"
    )

    raise AssertionError(
        "O sistema aceitou um contexto incorreto."
    )

except Exception as erro:
    if isinstance(erro, AssertionError):
        raise

    print("[OK] Proteção contra contexto incorreto")


print("\nTODOS OS TESTES FORAM CONCLUÍDOS!")

