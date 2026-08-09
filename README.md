# MoneBank - Actividad 3 (Componentes padre e hijo con TypeScript)

Proyecto React + TypeScript (Vite) que implementa las 5 interfaces pedidas:
`Usuarios` (Perfil/Cuenta), `Productos` (Bolsillos), `Login`, `Registro` y
`Transacciones`, todas usando un componente hijo reutilizable
(`CardAccion.tsx`) y comunicación por **props** (padre → hijo) y
**funciones callback** (hijo → padre), sin usar `useState` ni ningún otro hook.

## Cómo correrlo

```bash
npm install
npm run dev
```

Abre la URL que muestra la terminal (por defecto `http://localhost:5173`).

## Estructura

```
src/
  components/
    CardAccion.tsx      -> componente hijo reutilizable
  pages/
    Usuarios.tsx         -> interfaz Usuarios (Perfil/Cuenta)
    Productos.tsx        -> interfaz Productos (Bolsillos)
    Login.tsx             -> interfaz Login
    Registro.tsx          -> interfaz Registro
    Transacciones.tsx     -> módulo adicional elegido
  App.tsx                 -> navegación entre los 5 módulos
  main.tsx                -> punto de entrada
  styles/global.css        -> estilos (paleta de MoneBank)
```
