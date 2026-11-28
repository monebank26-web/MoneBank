ALTER TABLE public.usuario
  ADD COLUMN IF NOT EXISTS fecha_desbloqueo timestamp without time zone;

CREATE TABLE IF NOT EXISTS public.registro_accion_admin (
  id_registro_accion integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  id_admin integer NOT NULL,
  accion character varying(60) NOT NULL,
  id_usuario_afectado integer,
  detalle text,
  fecha timestamp with time zone DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_registro_accion_afectado
  ON public.registro_accion_admin USING btree (id_usuario_afectado);

CREATE INDEX IF NOT EXISTS ix_registro_accion_fecha
  ON public.registro_accion_admin USING btree (fecha);

CREATE TABLE IF NOT EXISTS public.modulo_sistema (
  id_modulo_sistema integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  clave character varying(40) NOT NULL UNIQUE,
  nombre character varying(80) NOT NULL,
  descripcion character varying(255),
  estado character varying(20) DEFAULT 'ACTIVO' NOT NULL,
  fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL,
  CONSTRAINT modulo_sistema_estado_check CHECK (estado IN ('ACTIVO', 'INACTIVO'))
);

CREATE TABLE IF NOT EXISTS public.limite_financiero_global (
  id_limite_financiero_global integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  clave character varying(60) NOT NULL UNIQUE,
  valor character varying(60) NOT NULL,
  fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS public.registro_error (
  id_registro_error integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tipo_error character varying(60) NOT NULL,
  clasificacion character varying(20) NOT NULL,
  mensaje character varying(500) NOT NULL,
  detalle text,
  metodo_http character varying(10),
  ruta character varying(255),
  codigo_http integer,
  id_usuario integer,
  fecha timestamp with time zone DEFAULT now() NOT NULL,
  CONSTRAINT registro_error_clasificacion_check CHECK (clasificacion IN ('NEGOCIO', 'VALIDACION', 'SISTEMA'))
);

CREATE INDEX IF NOT EXISTS ix_registro_error_fecha
  ON public.registro_error USING btree (fecha);

CREATE INDEX IF NOT EXISTS ix_registro_error_tipo
  ON public.registro_error USING btree (tipo_error);

CREATE TABLE IF NOT EXISTS public.mensaje_informativo (
  id_mensaje integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  titulo character varying(120) NOT NULL,
  contenido text NOT NULL,
  estado character varying(20) DEFAULT 'ACTIVO' NOT NULL,
  id_admin integer,
  fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
  fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL,
  CONSTRAINT mensaje_informativo_estado_check CHECK (estado IN ('ACTIVO', 'INACTIVO'))
);
