"""
Módulo Central do Tutor de Matemática: Gestão de Estado, Base de Dados e Autenticação.
Suporta persistência local leve, autenticação de alunos e anti-plágio de fotos.
"""

import os
import sqlite3
import hashlib
import unicodedata
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "dados", "tutor.db")

def hash_senha(senha: str) -> str:
    """Gera um hash SHA-256 seguro para a palavra-passe."""
    if not senha:
        return ""
    return hashlib.sha256(senha.strip().encode("utf-8")).hexdigest()

def inicializar_bd(db_path: str = DB_PATH):
    """Inicializa as tabelas da base de dados SQLite se não existirem e aplica migrações."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Tabela de alunos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        turma TEXT NOT NULL,
        username TEXT UNIQUE,
        password_hash TEXT,
        data_registo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Migrações na tabela alunos
    try:
        cursor.execute("ALTER TABLE alunos ADD COLUMN username TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_alunos_username ON alunos(username)")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE alunos ADD COLUMN password_hash TEXT")
    except sqlite3.OperationalError:
        pass

    # 2. Tabela de sessões de trabalho
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        ficha_id TEXT NOT NULL,
        estado_atual TEXT NOT NULL,
        data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_fim TIMESTAMP,
        FOREIGN KEY (aluno_id) REFERENCES alunos (id)
    )
    """)
    
    # 3. Tabela de tentativas e avaliações formativas passo a passo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tentativas_passos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        ficha_id TEXT NOT NULL,
        tipo TEXT NOT NULL, -- 'exemplo' ou 'exercicio'
        numero INTEGER NOT NULL,
        passo TEXT NOT NULL,
        resposta_aluno TEXT,
        caminho_foto TEXT,
        foto_hash TEXT,
        correto BOOLEAN NOT NULL,
        feedback_dado TEXT NOT NULL,
        pista_fornecida TEXT,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        duracao_segundos REAL DEFAULT 0,
        FOREIGN KEY (aluno_id) REFERENCES alunos (id)
    )
    """)
    
    # Migrações na tabela tentativas_passos
    try:
        cursor.execute("ALTER TABLE tentativas_passos ADD COLUMN duracao_segundos REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE tentativas_passos ADD COLUMN foto_hash TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE tentativas_passos ADD COLUMN ficha_id TEXT DEFAULT 'tarefa_07'")
    except sqlite3.OperationalError:
        pass

    # 4. Assegurar alunos iniciais de demonstração com credenciais
    cursor.execute("SELECT COUNT(*) FROM alunos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO alunos (id, nome, turma, username, password_hash)
        VALUES (1, 'Duarte Ferreira', '10.º A', 'duarte', ?)
        """, (hash_senha("1234"),))
        cursor.execute("""
        INSERT INTO alunos (id, nome, turma, username, password_hash)
        VALUES (2, 'Beatriz Santos', '10.º A', 'beatriz', ?)
        """, (hash_senha("1234"),))
    else:
        # Se os alunos existentes não tiverem credenciais, preencher com valores padrão
        cursor.execute("SELECT id, nome, username, password_hash FROM alunos")
        for aid, anome, auser, ahash in cursor.fetchall():
            if not auser:
                primeiro_nome = anome.split()[0].lower()
                cursor.execute("UPDATE alunos SET username = ? WHERE id = ?", (primeiro_nome, aid))
            if not ahash:
                cursor.execute("UPDATE alunos SET password_hash = ? WHERE id = ?", (hash_senha("1234"), aid))

    conn.commit()
    conn.close()

def autenticar_aluno(identificador: str, senha_plana: str, db_path: str = DB_PATH):
    """Autentica o aluno por username ou id e valida a palavra-passe."""
    if not identificador or not senha_plana:
        return None
    ident = identificador.strip().lower()
    hash_p = hash_senha(senha_plana)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, nome, turma, username, password_hash FROM alunos 
    WHERE LOWER(username) = ? OR CAST(id AS TEXT) = ? OR LOWER(nome) = ?
    """, (ident, ident, ident))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        stored_hash = row[4]
        # Se coincidir o hash ou senha padrão "1234"
        if stored_hash == hash_p or stored_hash == senha_plana or (not stored_hash and senha_plana == "1234"):
            return {
                "id": row[0],
                "nome": row[1],
                "turma": row[2],
                "username": row[3] or f"aluno_{row[0]}"
            }
    return None

def redefinir_senha_aluno(aluno_id: int, nova_senha: str, db_path: str = DB_PATH) -> bool:
    """Permite ao professor redefinir a palavra-passe de qualquer aluno."""
    if not nova_senha:
        return False
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE alunos SET password_hash = ? WHERE id = ?", (hash_senha(nova_senha), aluno_id))
    afetados = cursor.rowcount
    conn.commit()
    conn.close()
    return afetados > 0

def normalizar_slug(texto: str) -> str:
    """Remove acentos e caracteres especiais para gerar nomes de utilizador limpos."""
    t = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    t = ''.join(c if c.isalnum() or c in '._-' else '' for c in t.lower().strip())
    return t

def gerar_username_unico(nome: str, db_path: str = DB_PATH) -> str:
    """Gera um username único no formato nome.apelido a partir do nome completo."""
    partes = [p for p in nome.strip().split() if p]
    if not partes:
        base = "aluno"
    elif len(partes) == 1:
        base = normalizar_slug(partes[0])
    else:
        base = f"{normalizar_slug(partes[0])}.{normalizar_slug(partes[-1])}"
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    candidato = base
    contador = 1
    while True:
        c.execute("SELECT id FROM alunos WHERE LOWER(username) = ?", (candidato.lower(),))
        if not c.fetchone():
            break
        contador += 1
        candidato = f"{base}{contador}"
    conn.close()
    return candidato

def importar_alunos_lote(nomes: list, turma: str, senha_padrao: str = "1234", db_path: str = DB_PATH) -> list:
    """Importa uma lista de nomes para uma determinada turma, gerando credenciais automáticas."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    inseridos = []
    for nome in nomes:
        nome_limpo = nome.strip()
        if not nome_limpo:
            continue
        usr = gerar_username_unico(nome_limpo, db_path=db_path)
        pwd_hash = hash_senha(senha_padrao)
        c.execute("INSERT INTO alunos (nome, turma, username, password_hash) VALUES (?, ?, ?, ?)",
                  (nome_limpo, turma.strip(), usr, pwd_hash))
        novo_id = c.lastrowid
        inseridos.append({"id": novo_id, "nome": nome_limpo, "turma": turma.strip(), "username": usr})
    conn.commit()
    conn.close()
    return inseridos

def criar_aluno(nome: str, turma: str, username: str, senha: str, db_path: str = DB_PATH):
    """Cria um novo aluno na turma com as respetivas credenciais."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    u = username.strip().lower()
    cursor.execute("SELECT id FROM alunos WHERE LOWER(username) = ?", (u,))
    if cursor.fetchone():
        conn.close()
        raise ValueError(f"O nome de utilizador '{username}' já se encontra registado.")
    
    cursor.execute("""
    INSERT INTO alunos (nome, turma, username, password_hash)
    VALUES (?, ?, ?, ?)
    """, (nome.strip(), turma.strip(), u, hash_senha(senha)))
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return novo_id

def verificar_foto_duplicada(foto_bytes: bytes, aluno_id: int, db_path: str = DB_PATH):
    """
    Verifica se a fotografia já foi enviada anteriormente por OUTRO aluno (anti-plágio).
    Retorna (True, nome_autor_original) se for duplicada, ou (False, hash_calculado) se for inédita.
    """
    if not foto_bytes:
        return False, None
    f_hash = hashlib.sha256(foto_bytes).hexdigest()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT tp.aluno_id, al.nome 
    FROM tentativas_passos tp
    JOIN alunos al ON tp.aluno_id = al.id
    WHERE tp.foto_hash = ? AND tp.aluno_id != ?
    LIMIT 1
    """, (f_hash, aluno_id))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return True, row[1]
    return False, f_hash

def registar_tentativa(aluno_id: int, ficha_id: str, tipo: str, numero: int, passo: str,
                       resposta_aluno: str, correto: bool, feedback: str,
                       pista: str = None, caminho_foto: str = None, foto_hash: str = None,
                       duracao_segundos: float = 0, db_path: str = DB_PATH):
    """Regista uma interação e avaliação formativa na base de dados com métricas temporais e hash da foto."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tentativas_passos (
        aluno_id, ficha_id, tipo, numero, passo, resposta_aluno,
        caminho_foto, foto_hash, correto, feedback_dado, pista_fornecida, data_hora, duracao_segundos
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        aluno_id, ficha_id, tipo, numero, str(passo), resposta_aluno,
        caminho_foto, foto_hash, correto, feedback, pista, datetime.now().isoformat(), float(duracao_segundos or 0)
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_bd()
    print("Base de dados do tutor inicializada e migrada com sucesso em:", DB_PATH)
