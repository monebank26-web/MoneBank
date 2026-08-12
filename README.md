# MoneBank - Proyecto Bootcamp

Sistema de billetera digital con enfoque formativo orientado a la gestión y comprensión del dinero en un entorno simulado.

---

## 1️⃣ ¿Qué Problema Resuelve?

MoneBank es una billetera digital diseñada para jóvenes y personas sin experiencia financiera que necesitan aprender a gestionar su dinero. Muchas personas comienzan a manejar ingresos sin comprender el impacto real de sus decisiones, lo que genera hábitos financieros inadecuados.

El sistema permite simular la administración del dinero en un entorno controlado. Los usuarios pueden registrar ingresos, gastos y movimientos financieros, además de analizar el impacto de sus decisiones antes de ejecutarlas. Esto lo convierte en una herramienta de aprendizaje, no solo de gestión.

---

## 2️⃣ Usuarios Principales

1. **Usuario:** Registra ingresos, gastos y movimientos, consulta su historial y analiza el impacto de sus decisiones financieras.
2. **Parental:** Supervisa y controla los movimientos financieros de usuarios menores a su cargo.
3. **Menor:** Cuenta dependiente cuyos movimientos son gestionados o supervisados por un usuario parental.
4. **Independiente:** Usuario que administra su cuenta de manera autónoma sin supervisión.
5. **Administrador del sistema:** Gestiona usuarios, supervisa el funcionamiento general del sistema y controla la configuración administrativa.

---

## 3️⃣ Funcionalidades Principales

- [ ] Registro e inicio de sesión mediante autenticación JWT.
- [ ] Gestión del perfil de usuario.
- [ ] Gestión de cuentas y saldo interno.
- [ ] Registro de ingresos y gastos.
- [ ] Historial de movimientos financieros.
- [ ] Clasificación de movimientos por categorías.
- [ ] Evaluación previa del impacto financiero de un gasto.
- [ ] Dashboard con métricas y análisis financiero.
- [ ] Creación y administración de metas de ahorro.
- [ ] Programación automática de aportes a metas de ahorro.
- [ ] Sistema de control parental para supervisión y gestión de cuentas dependientes.
- [ ] Administración de usuarios por parte del administrador.
- [ ] Gestión de roles y permisos.
- [ ] Validación y control de acceso según el tipo de usuario.

---

## 4️⃣ Decisiones Iniciales

### Metodología de Desarrollo

**Elegimos:** Scrum

**¿Por qué?**

Permite desarrollar el proyecto de forma iterativa e incremental, facilitando la entrega continua de funcionalidades, la retroalimentación constante y la adaptación a nuevos requerimientos durante el desarrollo.

---

### Arquitectura

#### Backend

**Elegimos:** Arquitectura Limpia (Clean Architecture) modular.

**¿Por qué?**

El backend se encuentra dividido en módulos funcionales independientes (Usuarios, Autenticación, Cuentas, Movimientos, Ahorros, Control Parental, Analytics, entre otros), donde cada módulo implementa las capas de **Presentación**, **Aplicación**, **Dominio** e **Infraestructura**. Esta separación desacopla la lógica de negocio de los detalles técnicos, facilita el mantenimiento, mejora la escalabilidad, favorece las pruebas y permite reemplazar tecnologías de infraestructura con un impacto mínimo sobre el dominio.

#### Frontend

**Elegimos:** Arquitectura basada en Features.

**¿Por qué?**

El frontend está organizado por funcionalidades de negocio en lugar de por tipo de archivo. Cada feature encapsula sus páginas, componentes, hooks, servicios y lógica propia, mientras que un núcleo (**core**) concentra los elementos compartidos como rutas, contexto global, configuración de la API y constantes. Esta organización mejora la escalabilidad, reduce el acoplamiento y facilita el trabajo colaborativo del equipo.

---

### Tecnologías

- **Backend:** FastAPI
- **Frontend:** React
- **Base de Datos:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validación de datos:** Pydantic
- **Autenticación:** JWT (JSON Web Token)
- **Hash de contraseñas:** bcrypt
- **Control de versiones:** Git y GitHub

---

## 5️⃣ Resumen de la Arquitectura

MoneBank implementa una arquitectura cliente-servidor compuesta por tres capas principales:

- **Frontend:** Aplicación SPA desarrollada en React con arquitectura basada en Features para organizar cada funcionalidad de manera independiente.
- **Backend:** API REST desarrollada en FastAPI utilizando Arquitectura Limpia (Clean Architecture), organizada por módulos funcionales y dividida en las capas de Presentación, Aplicación, Dominio e Infraestructura.
- **Base de Datos:** PostgreSQL como sistema de persistencia relacional.

### Flujo General

```text
Usuario
   │
   ▼
Frontend (React)
   │ HTTP/JSON
   ▼
Backend (FastAPI)
   │ SQLAlchemy
   ▼
PostgreSQL
```

### Organización del Backend

Cada módulo sigue la siguiente estructura:

```text
Presentación
│
├── Router
└── Schemas

Aplicación
│
└── Services

Dominio
│
├── Entities
└── Interfaces

Infraestructura
│
├── Models
└── Repositories
```

junto a core y un shared organizado asi:
```text
Core
│
├── Config
├── Database
├── Dependencies
├── Security
└── Constants

Shared
│
├── Exceptions
├── Responses
└── Utils
```


### Organización del Frontend

Cada feature sigue la siguiente estructura:

```text
Feature
│
├── Pages
├── Components
├── Hooks
├── Services
└── Schemas
```
junto a un core:

```text
Core
│
├── API
├── Routes
├── Context
├── Constants
├── Hooks
└── Utils
```

### Principios de la Arquitectura

- Separación de responsabilidades.
- Arquitectura modular por dominios funcionales.
- Independencia entre la lógica de negocio y la infraestructura.
- Comunicación mediante interfaces.
- API REST para la comunicación entre frontend y backend.
- Seguridad mediante JWT y contraseñas cifradas con bcrypt.
- Acceso a la base de datos mediante repositorios y SQLAlchemy.
- Frontend organizado mediante arquitectura basada en Features.

Esta arquitectura facilita el mantenimiento, la escalabilidad, las pruebas y el desarrollo colaborativo del proyecto.

---

## 6️⃣ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Frontend | React |
| Backend | FastAPI |
| Base de Datos | PostgreSQL |
| ORM | SQLAlchemy |
| Validación | Pydantic |
| Autenticación | JWT |
| Hash de contraseñas | bcrypt |
| Control de versiones | Git + GitHub |

---

**Autores:** María Fernanda Calderón Lozano, David Santiago Camacho Cárdenas, Brayan Samuel Reyes Grimaldos, Tania Alejandra Suárez Ariza, Laura Andrea Velandia Farfán

**Fecha:** Abril 2026

**Bootcamp:** Arquitectura de Software - SENA

---

> *Documento en constante evolución conforme avanza el desarrollo del proyecto.*
