-- HU-0006: Tabla de tokens de recuperación de contraseña
-- Ejecutar una sola vez en la base de datos monebank

CREATE TABLE IF NOT EXISTS password_reset_token (
    id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario_id        INT NOT NULL,
    token_hash        VARCHAR(64) NOT NULL UNIQUE,
    fecha_creacion    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion  TIMESTAMP WITH TIME ZONE NOT NULL,
    usado             BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (usuario_id)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_reset_token_hash
    ON password_reset_token(token_hash);

CREATE INDEX IF NOT EXISTS idx_reset_token_usuario
    ON password_reset_token(usuario_id);
