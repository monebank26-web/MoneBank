// Iconos (Material Design Icons) por categoría.
//
// `iconoDeCategoria` busca por nombre normalizado (minúsculas, sin tildes y
// sin espacios al inicio/final), así que las claves van en minúsculas y sin
// tildes. Las claves con espacios corresponden a los nombres completos de la
// tabla `categoria`.
const ICONOS_POR_CATEGORIA = {
  // --- Nombres cortos y sinónimos (datos históricos del navegador) ---
  alimentacion: 'mdi:food',
  'alimentacion-fuera-de-casa': 'mdi:silverware-fork-knife',
  alimentos: 'mdi:food',
  comida: 'mdi:food',
  restaurante: 'mdi:silverware-fork-knife',
  restaurantes: 'mdi:silverware-fork-knife',
  supermercado: 'mdi:cart-outline',
  mercado: 'mdi:cart-outline',
  transporte: 'mdi:bus',
  'transporte-publico': 'mdi:bus',
  gasolina: 'mdi:gas-station',
  combustible: 'mdi:gas-station',
  salud: 'mdi:medical-bag',
  medicamentos: 'mdi:medical-bag',
  farmacia: 'mdi:medical-bag',
  farmacias: 'mdi:medical-bag',
  educacion: 'mdi:school-outline',
  vivienda: 'mdi:home-outline',
  arriendo: 'mdi:home-currency-usd',
  servicios: 'mdi:receipt',
  'servicios-publicos': 'mdi:receipt',
  energia: 'mdi:lightning-bolt',
  luz: 'mdi:lightning-bolt',
  agua: 'mdi:water-outline',
  internet: 'mdi:wifi',
  telefono: 'mdi:cellphone',
  entretenimiento: 'mdi:movie-open-outline',
  cine: 'mdi:filmstrip',
  juegos: 'mdi:gamepad-variant-outline',
  salario: 'mdi:briefcase-outline',
  nomina: 'mdi:briefcase-outline',
  sueldo: 'mdi:briefcase-outline',
  ropa: 'mdi:tshirt-crew-outline',
  vestimenta: 'mdi:tshirt-crew-outline',
  shopping: 'mdi:shopping-outline',
  viajes: 'mdi:airplane',
  viaje: 'mdi:airplane',
  vacaciones: 'mdi:airplane',
  ahorro: 'mdi:piggy-bank',
  ahorros: 'mdi:piggy-bank',
  meta: 'mdi:piggy-bank',
  mascotas: 'mdi:paw',
  mascota: 'mdi:paw',
  regalos: 'mdi:gift-outline',
  regalo: 'mdi:gift-outline',
  donacion: 'mdi:heart-outline',
  impuestos: 'mdi:file-document-outline',
  deporte: 'mdi:dumbbell',
  gimnasio: 'mdi:dumbbell',
  gym: 'mdi:dumbbell',

  // --- Nombres completos de las categorías de la base de datos ---
  // Ingresos
  ventas: 'mdi:storefront-outline',
  'mesada parental recibida': 'mdi:hand-coin-outline',
  freelance: 'mdi:laptop-account',
  honorarios: 'mdi:account-cash-outline',
  bonificaciones: 'mdi:cash-plus',
  'prima y cesantias': 'mdi:cash-plus',
  arriendos: 'mdi:home-city-outline',
  inversiones: 'mdi:chart-line',
  pension: 'mdi:account-clock-outline',
  'becas y subsidios': 'mdi:school-outline',
  'regalos y donaciones': 'mdi:gift-outline',
  reembolsos: 'mdi:cash-refund',
  'venta de articulos': 'mdi:tag-multiple-outline',
  'otros ingresos': 'mdi:cash-multiple',

  // Gastos
  'mesada parental enviada': 'mdi:hand-coin-outline',
  'vivienda y arriendo': 'mdi:home-city-outline',
  'restaurantes y domicilios': 'mdi:silverware-fork-knife',
  'ropa y calzado': 'mdi:tshirt-crew-outline',
  'cuidado personal': 'mdi:spa-outline',
  'tecnologia y electronicos': 'mdi:laptop',
  suscripciones: 'mdi:calendar-sync',
  'internet y telefonia': 'mdi:wifi',
  'hogar y muebles': 'mdi:sofa-outline',
  seguros: 'mdi:shield-check-outline',
  'deudas y prestamos': 'mdi:credit-card-outline',
  'hijos y familia': 'mdi:human-male-child',
  'deportes y gimnasio': 'mdi:dumbbell',
  'viajes y turismo': 'mdi:airplane',
  'mantenimiento de vehiculo': 'mdi:car-wrench',
  'otros gastos': 'mdi:dots-horizontal-circle-outline',

  // Ahorros
  tecnologia: 'mdi:laptop',
  vehiculo: 'mdi:car',
  emergencia: 'mdi:alert-octagon-outline',
  otro: 'mdi:dots-horizontal-circle-outline',
  jubilacion: 'mdi:beach',
  inversion: 'mdi:chart-line',
  negocio: 'mdi:store',
  'boda o evento': 'mdi:ring',
  'pago de deudas': 'mdi:credit-card-check-outline',
};

const ICONO_DEFECTO = 'mdi:tag-outline';

const normalizar = (nombre = '') =>
  nombre.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();

export const iconoDeCategoria = (nombreCategoria) =>
  ICONOS_POR_CATEGORIA[normalizar(nombreCategoria)] || ICONO_DEFECTO;
