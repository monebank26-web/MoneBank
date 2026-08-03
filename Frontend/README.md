# MoneBank

MoneBank es una aplicación web que desarrollé utilizando React. La idea principal del proyecto es simular una banca digital donde los usuarios puedan administrar su dinero de una forma sencilla, crear bolsillos de ahorro, realizar movimientos y llevar un mejor control de sus finanzas.

Para este proyecto decidí trabajar sin un backend, por lo que toda la información se guarda directamente en el `localStorage` del navegador. Allí se almacenan los usuarios, los saldos, los bolsillos y todas las transacciones, permitiendo que la aplicación funcione de manera completamente local.

## Cómo ejecutar el proyecto

```bash
npm install
npm start
```

Después de ejecutar estos comandos, la aplicación estará disponible en:

```
http://localhost:3000
```

## ¿Cómo organicé el proyecto?

Quise mantener el código organizado para que fuera fácil de entender y de seguir ampliando. Por eso dividí la aplicación en tres carpetas principales:

```
src/
├── core/            → Aquí está toda la configuración general del proyecto, las rutas, constantes, el contexto de autenticación y el cliente API.
├── shared/          → En esta carpeta coloqué los componentes y layouts que se reutilizan en diferentes partes de la aplicación.
└── features/        → Aquí separé cada funcionalidad en módulos independientes, como autenticación, dashboard, bolsillos, transacciones, control parental, administrador y perfil.
```

Todas las páginas privadas utilizan el mismo diseño principal (`MainLayout`), que incluye el menú lateral y el encabezado para mantener una navegación consistente.

---

# Funcionalidades de la aplicación

## Inicio de sesión

La página de Login permite que un usuario ingrese utilizando su correo y contraseña. Cuando las credenciales son correctas, la sesión se guarda automáticamente y el usuario es enviado al Dashboard. Si ya tenía una sesión iniciada, no necesita volver a autenticarse.

---

## Registro

El registro está dividido en dos pasos para hacerlo más claro.

Primero se solicitan los datos básicos como el nombre, correo, contraseña y saldo inicial.

Después el usuario puede escoger qué tipo de cuenta desea crear: usuario normal, padre o hijo. En caso de elegir hijo, también se pregunta si es menor de edad para habilitar posteriormente el control parental.

Además, si el correo registrado corresponde al administrador definido en el sistema, la cuenta obtiene automáticamente ese rol.

---

## Dashboard

Esta es la primera pantalla que el usuario ve después de iniciar sesión.

Aquí decidí mostrar la información más importante de forma rápida:

- Un saludo personalizado según la hora del día.
- El saldo disponible en la cuenta principal.
- La opción para consignar dinero.
- El dinero total que el usuario tiene guardado en sus bolsillos.
- Accesos rápidos a los bolsillos.
- Las últimas cinco transacciones realizadas.

La idea es que el usuario pueda conocer el estado de su cuenta apenas ingrese.

---

## Bolsillos

En esta sección el usuario puede crear bolsillos de ahorro personalizados.

Cada bolsillo tiene su propio nombre, color, descripción y saldo.

Desde esta misma página es posible:

- Crear nuevos bolsillos.
- Agregar dinero.
- Transferir dinero entre bolsillos.
- Entrar al detalle de cada bolsillo.

---

## Detalle de bolsillo

Cada bolsillo tiene su propia página.

Aquí el usuario puede ver toda la información relacionada con ese bolsillo, incluyendo:

- Nombre.
- Descripción.
- Color.
- Saldo.
- Historial de movimientos.

También puede agregar dinero, transferir fondos, editar la información o eliminar el bolsillo.

Si el bolsillo ya no existe, la aplicación muestra un mensaje indicando que fue eliminado y permite regresar al listado.

---

## Transacciones

Esta sección muestra el historial completo de movimientos realizados por el usuario.

Incluye consignaciones, depósitos, transferencias y cualquier otra operación realizada dentro de la aplicación.

También agregué filtros para que sea más fácil encontrar un tipo específico de movimiento.

---

## Control parental

Esta funcionalidad cambia dependiendo del tipo de usuario.

### Padre o madre

Puede vincular la cuenta de un hijo utilizando su correo electrónico.

Después de realizar la vinculación puede consultar:

- El saldo del hijo.
- Sus bolsillos.
- Sus últimos movimientos.

### Hijo

Puede vincularse con la cuenta de uno de sus padres mediante el correo electrónico y visualizar un aviso indicando que su cuenta está siendo supervisada.

Inicialmente ambas vistas estaban en una sola página, pero decidí separarlas para que cada una tuviera su propia ruta y fuera mucho más sencilla de mantener.

---

## Panel de administrador

Esta página solo está disponible para los administradores.

Desde aquí es posible gestionar todos los usuarios registrados.

El administrador puede:

- Buscar usuarios.
- Filtrarlos por rol.
- Ver su información.
- Editarlos.
- Eliminarlos.

---

## Mi perfil

En esta sección cada usuario puede administrar su propia información.

Aquí puede consultar sus datos personales, editar su nombre y correo electrónico y cambiar la contraseña mediante un modal que primero verifica la contraseña actual antes de guardar la nueva.

También agregué un pequeño resumen con el nombre, correo, rol y saldo para que el usuario tenga toda su información reunida en un solo lugar.

---

# Componentes compartidos

Durante el desarrollo reutilicé varios componentes para evitar repetir código.

Entre los principales están:

- **MainLayout**, que contiene el menú lateral, el encabezado y el botón para cerrar sesión.
- **Modal**, utilizado en diferentes módulos como Dashboard, Bolsillos, Administrador y Perfil.
- **AuthContext**, encargado de manejar toda la información de la sesión del usuario.
- **authService**, donde centralicé toda la lógica relacionada con autenticación, registro, actualización de datos y control de roles.
- **bolsillosService**, donde implementé toda la lógica para administrar los bolsillos y las transacciones.

---

# Roles disponibles

La aplicación cuenta con cuatro tipos de usuarios.

| Rol | Función |
|------|----------|
| **Normal** | Puede administrar su cuenta, bolsillos, transacciones y perfil. |
| **Padre** | Además de las funciones normales, puede supervisar la cuenta de un hijo. |
| **Hijo** | Puede vincular su cuenta con un padre para ser supervisado. |
| **Administrador** | Administra todos los usuarios registrados en la plataforma. |

---

# Algunas consideraciones

Como este proyecto fue realizado con fines académicos, decidí guardar toda la información en el `localStorage`, por lo que no fue necesario desarrollar un backend.

De la misma manera, las contraseñas también se almacenan allí en texto plano. Soy consciente de que esta práctica no sería adecuada para una aplicación real, pero para el objetivo del proyecto permitió concentrarme en la lógica de la aplicación y en la experiencia del usuario sin depender de un servidor.