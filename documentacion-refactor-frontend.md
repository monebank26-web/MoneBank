# Refactor de componentes y hooks — MoneBank Frontend

Este documento resume qué se cambió hoy en el frontend, por qué, y cómo aplicar
los cambios a tu proyecto local antes de hacer commit y push.

## El problema que se resolvió

Varias páginas dentro de `src/features/*/pages/` tenían **todo mezclado**:
estado (`useState`, `useEffect`), lógica de negocio (llamadas a `services`,
validaciones) y JSX, todo en un solo archivo. Eso hacía que:

- Los archivos fueran gigantes (algunos de 200+ líneas).
- Funciones como `formatMoney`, `formatFecha` y `etiquetaRol` estuvieran
  copiadas y pegadas en 6-8 archivos distintos, con pequeñas diferencias.
- Fuera difícil reusar una parte visual (ej. una tarjeta) en otro lugar.

## El patrón que se aplicó en todas las páginas

1. **Toda la lógica** (estado + llamadas a `services`) se movió a uno o más
   **hooks personalizados** en `features/<feature>/hooks/useAlgo.js`. El hook
   retorna un objeto con el estado y las funciones que la página necesita.
2. **Cada bloque visual independiente** (una tarjeta, un modal, una fila de
   tabla) se movió a un **componente** en `features/<feature>/components/`.
   Estos componentes solo reciben `props` y pintan JSX — no tienen `useState`
   propio relacionado con lógica de negocio.
3. **La página (`pages/Algo.jsx`)** quedó reducida a: llamar los hooks y
   acomodar los componentes en el layout. Nada de lógica ahí.
4. Cosas repetidas en varios archivos (`formatMoney`, `formatFecha`,
   `etiquetaRol`) se centralizaron en `core/utils/`.

Todos los nombres se pusieron en **español, completos, sin abreviar ni
mezclar inglés** (ej. `ModalCrearBolsillo`, no `CreateModal`).

---

## Utilidades compartidas nuevas (`core/utils/`)

| Archivo | Qué tiene | Antes estaba duplicado en |
|---|---|---|
| `format.js` | `formatMoney`, `formatFecha`, `formatFechaConHora` | 8 páginas distintas |
| `roles.js` | `etiquetaRol(rol)` → texto legible del rol (👑 Administrador, etc.) | `admin` (función) y `perfil` (objeto) |
| `saludo.js` | `obtenerSaludoSegunHora()` → "Buenos días/tardes/noches" | solo estaba en `dashboard`, se sacó por prolijidad |

---

## Página por página

### 1. `features/perfil/pages/PerfilPage.jsx` (283 → 55 líneas)
- `hooks/useDatosPersonales.js` → editar nombre/email.
- `hooks/useCambiarPassword.js` → modal de cambio de contraseña.
- `components/TarjetaResumenPerfil.jsx` → avatar, nombre, rol, saldo.
- `components/SeccionDatosPersonales.jsx` → vista + formulario de edición.
- `components/ModalCambiarPassword.jsx` → el modal de contraseña.

### 2. `features/bolsillos/pages/BolsillosPage.jsx` (201 → 90 líneas)
- `hooks/useModalesBolsillos.js` → maneja los 5 modales de la página.
- `components/MenuOpcionesBolsillo.jsx` → menú de tres puntos.
- `components/ModalCrearBolsillo.jsx` → crear bolsillo nuevo.
- `components/TarjetaBolsillo.jsx` → cada tarjeta de la lista.
- `components/ModalConfirmarEliminarBolsillo.jsx` → confirmación de borrado.

### 3. `features/admin/pages/AdminPage.jsx` (254 → 85 líneas)
- `hooks/useUsuariosAdmin.js` → carga usuarios, búsqueda, filtro por rol.
- `hooks/useAccionesUsuarioAdmin.js` → modales de ver/editar/eliminar usuario.
- `components/BarraFiltrosUsuarios.jsx` → buscador + filtros de rol.
- `components/FilaUsuarioAdmin.jsx` → cada fila de la tabla.
- `components/ModalDetalleUsuario.jsx`, `ModalEditarUsuario.jsx`,
  `ModalEliminarUsuario.jsx` → un modal por acción.

### 4. `features/bolsillos/pages/BolsilloDetallePage.jsx` (189 → 100 líneas)
- `hooks/useDetalleBolsillo.js` → carga el bolsillo y su historial, y
  recarga después de editar/depositar/transferir.
- `components/CabeceraDetalleBolsillo.jsx` → nombre, saldo, botones de acción.
- `components/ListaMovimientosBolsillo.jsx` → historial de movimientos.
- `components/ModalConfirmarEliminarDetalleBolsillo.jsx` → confirmación.

### 5. `features/controlParental/pages/ControlParentalPadrePage.jsx` (189 → 66 líneas)
### 6. `features/controlParental/pages/ControlParentalHijoPage.jsx` (128 → 64 líneas)

Estas dos páginas eran casi un espejo una de la otra, así que además de
separar lógica y vista, **se compartieron componentes** entre ambas:

- `hooks/useVinculacionHijo.js` → lógica del lado del padre/madre.
- `hooks/useVinculacionPadre.js` → lógica del lado del hijo/hija.
- `components/TarjetaVincularCuenta.jsx` → formulario para vincular,
  genérico (recibe ícono, título, descripción y placeholder por props, así
  que sirve para los dos sentidos de vinculación).
- `components/TarjetaCuentaVinculada.jsx` → tarjeta con la cuenta ya
  vinculada, genérico (recibe `children` para que cada página meta su
  contenido extra: el padre mete saldo/bolsillos, el hijo mete un texto
  informativo).
- `components/CuadriculaBolsillosHijo.jsx`, `ListaMovimientosHijo.jsx` →
  solo los usa la página del padre.

### 7. `features/dashboard/pages/DashboardPage.jsx` (159 → 54 líneas)
- `hooks/useConsignarSaldo.js` → modal de consignar dinero a Mi Cuenta.
- `hooks/useMovimientosRecientes.js` → carga los últimos movimientos.
- `components/TarjetasSaldoInicio.jsx` → las dos tarjetas de saldo.
- `components/SeccionBolsillosInicio.jsx` → miniatura de bolsillos.
- `components/SeccionMovimientosInicio.jsx` → lista de movimientos.
- `components/ModalConsignar.jsx` → modal de consignar.

---

## Pendientes que noté pero no toqué

1. **Typo en CSS:** `DashboardPage.css` tiene la clase
   `punto-bolsillo-miniaturaatura` (debería ser `miniatura`), repetida 3
   veces. Se dejó el JSX igual al CSS para no romper el estilo. Si la
   corriges, arréglala en los dos archivos a la vez.
2. **`ControlParentalPadrePage` lee `localStorage` directo** (`mb_bolsillos`,
   `mb_transacciones`) en vez de usar un `service`, como sí hace el resto
   del proyecto. Quedaría mejor moverlo a un `parentalService`, pero no se
   tocó para no cambiar comportamiento sin que lo revisaras.

---

## Cómo aplicar esto a tu proyecto local

Recibiste 5 archivos `.zip` en el chat, cada uno con archivos nuevos o
modificados, con las **mismas rutas relativas** que tiene tu proyecto:

1. `perfil-refactor.zip`
2. `bolsillos-refactor.zip`
3. `admin-refactor.zip`
4. `detalle-parental-dashboard-refactor.zip`
5. `control-parental-hijo-refactor.zip`

Pasos:

1. Descarga los 5 zips a una carpeta cualquiera.
2. Descomprime **cada uno** directamente dentro de tu carpeta
   `MoneBank/Frontend/src`, permitiendo que sobrescriba los archivos que ya
   existen (nombres repetidos = versión nueva).
   - En Windows: seleccionas el contenido del zip, copias, y pegas dentro de
     `Frontend/src`, aceptando "Reemplazar" cuando lo pida.
   - En Mac/Linux, desde la carpeta del zip:
     ```
     unzip -o perfil-refactor.zip -d /ruta/a/tu/MoneBank/Frontend/src
     ```
     (repite con cada zip, cambiando el nombre del archivo).
3. Abre el proyecto y corre `npm start` (o el comando que uses) para
   confirmar que todo carga bien antes de hacer commit.
4. Revisa con `git status` que los archivos nuevos aparecen como
   `Untracked` (los `hooks/` y `components/` nuevos) y los que edité como
   `modified` (las `pages/*.jsx` y `core/utils/*`).
5. Sigue el flujo que ya conoces:
   ```
   git add .
   git commit -m "refactor: separar componentes y hooks en perfil, bolsillos, admin, control parental y dashboard"
   git pull origin desarrollo
   ```
   Si el `pull` marca conflictos, mejor los revisamos juntos mañana antes de
   resolverlos, porque tu compañero también tocó código.
   ```
   git push origin <tu-rama>
   ```
