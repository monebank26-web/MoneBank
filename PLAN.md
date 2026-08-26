# PLAN — Alineación Front ↔ Backend MoneBank

> Fecha: 2026-08-24 · Estado: aprobado para ejecución por fases

## Principios rectores

1. **El backend es la fuente de verdad** para nombres de campos (`nombres`, `apellidos`, `correo`, `id_rol`, `saldo`).
2. **Endpoints nuevos:** solo se diseñan en un documento, no se implementan.
3. **Carpetas vacías se conservan;** el plan indica qué recibirán en el futuro.
4. **Metas y Límites** = features nuevas con componentes propios; **Bolsillos** sigue siendo su propia feature.

---

## Contexto actual (verificado en el repo)

### Frontend (`Frontend/src/`)
| Zona | Estado |
|------|--------|
| `core/api/client.js` | Sin soporte de query params |
| `core/constants/index.js` | `ROLES` como strings, no IDs del backend |
| `core/context/AuthContext.jsx` | Shape de usuario desalineado del `LoginResponse` real |
| `features/bolsillos` | Feature completa y funcional (se mantiene) |
| `features/dashboard`, `perfil`, `admin`, `transacciones`, `controlParental` | Operan con datos mock / localStorage / llamadas fantasma |
| Carpetas vacías reservadas | `notification/`, `parental_control/`, `saving/`, `transaction/` |

### Backend (`Backend/`)
FastAPI con implementados: **auth**, **usuarios**, **cuentas**, **transacciones**, **ahorros** (metas + límites). Pendientes: **control parental**, **notificaciones**, **ingresos**, **analytics**, **programación de ahorro**.

---

## FASE 1 — Core (fundación)

| Archivo | Cambio |
|---------|--------|
| `core/api/client.js` | Agregar soporte de query params: `get(endpoint, params)` para filtros del historial |
| `core/constants/index.js` | Reemplazar `ROLES` string por IDs del backend: `ROLES = {ADMIN:1, USUARIO:2}`, `TIPOS_USUARIO = {PADRE:1, HIJO:2, INDEPENDIENTE:3}`, `PERIODOS_LIMITE = ['DIARIO','SEMANAL','MENSUAL']` |
| `core/context/AuthContext.jsx` | User unificado: `{id_usuario, nombres, apellidos, correo, id_rol}` (shape exacto del `LoginResponse`) |
| `core/utils/roles.js` | `etiquetaRol(id_rol)` recibe número |
| `core/routes/router.jsx` | Guards comparan `user.id_rol === 1`; rutas nuevas `/metas` y `/limites` |

### Servicio auth — remapeo según `LoginResponse` real
```
{access_token, usuario_id, id_rol, nombres, apellidos, correo}
  → user: {id_usuario: usuario_id, nombres, apellidos, correo, id_rol} + token
```
- `register`: solo envía `{nombres, apellidos, correo, contrasena}`.

⚠️ El back **NO** devuelve `id_tipo_usuario` en login ni acepta tipo de cuenta en registro → la UI del wizard (padre/hijo/menor) se conserva visualmente pero queda marcada como pendiente de backend (diseño incluido en doc).

🔀 **Alternativa:** tras login hacer `GET /usuarios/{id}` para traer el usuario completo con `id_tipo_usuario`.

### Validación de contraseña en cliente
Replicar la política del back (**≥8 caracteres, mayúscula, minúscula, número, especial**) en Register y cambio de password, para evitar 422.

---

## FASE 2 — Servicios nuevos (uno por módulo del back)

| Servicio nuevo | Consume |
|----------------|---------|
| `cuentasService.js` | `GET /cuentas/` (saldo real), `POST /cuentas/` |
| `transaccionesService.js` | `GET /transacciones/historial` (paginado+filtros), `GET /categorias`, `GET /{id}`, `POST /gastos`, `POST /ahorros` |
| `metasService.js` | `POST/GET /ahorros/metas`, `GET /ahorros/{id}/progreso` |
| `limitesService.js` | `POST/GET /ahorros/limites`, `GET /ahorros/limites/alertas` |

Se **elimina `registrarGasto` de `authService`** (no pertenece ahí — transacciones fuera de su feature).

---

## FASE 3 — Dashboard

- **Saldo real:** hook nuevo `useSaldoCuenta()` → `GET /cuentas/` (reemplaza `user.saldoCuenta`, que nunca llegó del back).
- **Movimientos recientes:** `useMovimientosRecientes` pasa de localStorage a `GET /transacciones/historial?por_pagina=5`; `SeccionMovimientosInicio` se adapta al shape real (`tipo_transaccion`, `nombre_categoria`, `monto`, `fecha`).
- **Cards nuevas de acceso rápido:** componente `AccesoRapidoAhorros` con 3 cards → Metas, Límites, Bolsillos.
- **ModalConsignar:** 🔀 sin endpoint de ingresos aún → opción A: dejarlo deshabilitado con aviso "Próximamente"; opción B: quitarlo hasta que exista el endpoint.

---

## FASE 4 — Feature Metas (NUEVA, `features/metas/`)

### Campos exigidos por `MetaCreate` → formulario `ModalCrearMeta`

| Campo | Input |
|-------|-------|
| `nombre` | texto |
| `monto_objetivo` | number |
| `saldo_inicial` | number opcional |
| `fecha_objetivo` | date picker |
| `id_categoria` | select (categorías tipo AHORRO de `GET /categorias`) |

### Componentes
- `TarjetaMeta` — barra `porcentaje_completado`, `monto_faltante`, `fecha_objetivo`, estado `ACTIVO/PAUSADO/FINALIZADO`
- `ModalCrearMeta`
- `ModalAbonarMeta` — usa `POST /transacciones/ahorros`: monto + fecha + descripción + `id_ahorro`
- `ListaMetas`
- Hook: `useMetas`

---

## FASE 5 — Feature Límites (NUEVA, `features/limites/`)

### Formulario `ModalCrearLimite` según `LimiteCreate`

| Campo | Input |
|-------|-------|
| `nombre` | texto opcional (máx 100) |
| `monto_limite` | number > 0 |
| `periodo` | select DIARIO/SEMANAL/MENSUAL |
| `id_categoria` | select (categorías tipo GASTO) |

### Componentes
- `TarjetaLimite` — barra `porcentaje_usado`, `gasto_actual` vs `monto_limite`, `monto_disponible`
- `ListaAlertas` — consume `GET /ahorros/limites/alertas` → banner PREVENTIVA ≥80% / LIMITE_SUPERADO
- Manejo de error **422 presupuesto duplicado**
- Hook: `useLimites`

---

## FASE 6 — Página Transacciones (refactor total)

Pasa de localStorage a API real:

- **`BarraFiltrosTransacciones` (nuevo):** búsqueda, categoría (select dinámico), tipo, fecha inicio/fin, monto min/max, ordenar por fecha/monto asc/desc — todos opcionales, mapean 1:1 a `HistorialRequest`.
- **Paginación real:** `pagina`/`por_pagina`/`total_paginas`.
- Click en movimiento → **`ModalDetalleTransaccion`** (`GET /transacciones/{id}`).
- **Formulario RegistrarGasto:** monto > 0, fecha (date), descripción, categoría (select), cuenta propia automática.
- Items renderizan shape real: `tipo_transaccion`, `nombre_categoria`, `descripcion`, `estado_transaccion`.

---

## FASE 7 — Admin

- Corregir bugs: `await` faltantes en `cargarUsuarios` / `guardarEdicion` / `eliminarUsuario`.
- Renombrar props internos: `nombre→nombres`, `apellidos`, `email→correo` en `FilaUsuarioAdmin`, `ModalDetalleUsuario`, `ModalEditarUsuario`, `BarraFiltrosUsuarios` (busca por nombres/apellidos/correo).
- `ModalEditarUsuario`: solo permite editar lo que `PUT /usuarios/{id}` acepta (`nombres`, `apellidos`, `correo`); `saldoCuenta` y rol pasan a solo lectura (el back no los modifica vía ese endpoint). 🔀 **Alternativa:** ocultarlos del modal.
- Saldos de cada usuario: `GET /cuentas/?usuario_id={id}` para pintar la columna saldo.

---

## FASE 8 — Perfil

- `useDatosPersonales`: campos nombres/apellidos/correo, `PUT /usuarios/{id_usuario}`, refresca AuthContext al guardar.
- `useCambiarPassword`: firma corregida (`contrasena_actual`, `contrasena_nueva`) — hoy llama `(user.id, actual, nueva)` y crashea.
- `TarjetaResumenPerfil`: saldo desde `cuentasService`, nombres del shape unificado.

---

## FASE 9 — ControlParental (estabilizar sin backend)

Hoy llama a métodos inexistentes (`vincularCuentas`, `obtenerUsuarioPorCorreo`). Como el módulo back está vacío:

- Neutralizar las llamadas fantasma; la tarjeta de vincular queda con aviso "Disponible próximamente".
- 🔀 **Alternativa:** mantener el modo demo con localStorage actual pero encapsulado en un `parentalService`.

---

## FASE 10 — Documento de diseño de endpoints nuevos (SOLO diseño)

Nuevo archivo `docs/diseno-endpoints-faltantes.md` con especificación completa (método, ruta, body, response, permisos, errores):

1. `POST /transacciones/ingresos` — consignaciones (habilita ModalConsignar)
2. Módulo `control_parental`: tabla vinculacion, `POST /vinculaciones {correo}`, `GET /vinculaciones`, `GET /hijos/{id}/resumen`, `GET /hijos/{id}/transacciones`, `DELETE /vinculaciones/{id}`
3. Registro con tipo: extender `UsuarioCreate` con `id_tipo_usuario` opcional (+`es_menor`)
4. `PATCH /cuentas/{id}` — ajuste de saldo/estado
5. Módulo `programacion_ahorro`: aportes automáticos (`{id_ahorro, monto, frecuencia, dia}`, activar/pausar)
6. Módulo `analytics`: `GET /resumen`, `GET /tendencias` (para dashboard futuro)
7. Notificaciones: `GET /notificaciones` (unificaría alertas + recordatorios)

---

## FASE 11 — Roadmap de carpetas reservadas (documentado, no implementado)

| Carpeta | Historia pendiente que vivirá ahí |
|---------|-----------------------------------|
| `notification/` | Campana de notificaciones (mientras tanto puede alimentarse de `/ahorros/limites/alertas` que YA existe) |
| `transaction/` | Formularios standalone de ingresos cuando exista el endpoint |
| `parental_control/` | Consumo real cuando exista el módulo back |
| `saving/` | Hub unificado de los 3 tipos de ahorro |

---

## Decisiones abiertas (🔀) — resolver antes de implementar la fase correspondiente

| # | Fase | Decisión | Opciones |
|---|------|----------|----------|
| 1 | F1/F3 | Obtener `id_tipo_usuario` tras login | Wizard visual pendiente de backend **vs** llamar `GET /usuarios/{id}` post-login |
| 2 | F3 | ModalConsignar sin endpoint de ingresos | Deshabilitado con aviso "Próximamente" **vs** ocultarlo hasta que exista el endpoint |
| 3 | F7 | Campos no editables en ModalEditarUsuario | Mostrar como solo lectura **vs** ocultarlos del modal |
| 4 | F9 | ControlParental sin backend | Neutralizar con aviso "Disponible próximamente" **vs** modo demo localStorage encapsulado en `parentalService` |

---

## Riesgos identificados

| Riesgo | Mitigación prevista en el plan |
|--------|-------------------------------|
| Errores 422 por política de contraseña distinta entre cliente y back | Replicar la política exacta (≥8, mayúscula, minúscula, número, especial) en Register y cambio de password (F1) |
| `useCambiarPassword` crashea hoy (firma incorrecta `(user.id, actual, nueva)`) | Corregir firma a `(contrasena_actual, contrasena_nueva)` (F8) |
| Llamadas fantasma en controlParental (`vincularCuentas`, `obtenerUsuarioPorCorreo`) | Neutralización con aviso "Próximamente" o demo encapsulado (F9) |
| Presupuestos duplicados sin manejo explícito en UI | Capturar error 422 específico en `ModalCrearLimite` (F5) |
| Campos con nombres viejos propagándose (nombre/email/saldoCuenta) | Renombrado sistemático en Admin + shape unificado desde F1 |
| Datos mock/localStorage persistiendo tras migración | Cada fase reemplaza explícitamente su fuente (F3, F6, F8) |

---

## Orden de ejecución sugerido

```
F1 Core ──► F2 Servicios ──┬──► F3 Dashboard ─► F4 Metas ─┐
                           │                              ├──► F10 Doc endpoints
                           ├──► F6 Transacciones          │    F11 Roadmap carpetas
                           ├──► F7 Admin                  │    (documentación, puede
                           ├──► F8 Perfil                 │     ir en paralelo)
                           ├──► F9 ControlParental        │
                           └──► F5 Límites ───────────────┘
```

| Bloque | Fases | Nota |
|--------|-------|------|
| Crítico secuencial | F1 → F2 | Todo lo demás depende del client con query params, constantes con IDs y servicios nuevos |
| Paralelizable | F3–F9 | Una vez F1+F2 listas, las fases son independientes entre sí |
| Solo documentación | F10, F11 | Sin dependencia de código; pueden redactarse en cualquier momento |

**Recomendación:** ejecutar F1+F2+F3 primero (desbloquea saldo real e historial real), luego F4/F5 (features nuevas), después F6–F9 (refactors), y cerrar con F10/F11.
