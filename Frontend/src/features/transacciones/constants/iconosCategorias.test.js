import { iconoDeCategoria } from './iconosCategorias';

const ICONO_DEFECTO = 'mdi:tag-outline';

// Nombres tal como están en la tabla `categoria` (56 filas). Hay nombres que
// se repiten entre tipos (Educación, Salud, Hogar y muebles, Hijos y familia,
// Regalos y donaciones, Mascotas) y se listan repetidos a propósito: el test
// debe cubrir las 56 categorías reales, no solo las distintas.
const CATEGORIAS_DE_LA_BD = [
  'Salario',
  'Ventas',
  'Alimentación',
  'Transporte',
  'Educación',
  'Salud',
  'Entretenimiento',
  'Servicios',
  'Viaje',
  'Vivienda',
  'Vehículo',
  'Educación',
  'Tecnología',
  'Emergencia',
  'Salud',
  'Otro',
  'Mesada parental enviada',
  'Mesada parental recibida',
  'Freelance',
  'Honorarios',
  'Bonificaciones',
  'Prima y cesantías',
  'Arriendos',
  'Inversiones',
  'Pensión',
  'Becas y subsidios',
  'Regalos y donaciones',
  'Reembolsos',
  'Venta de artículos',
  'Otros ingresos',
  'Vivienda y arriendo',
  'Restaurantes y domicilios',
  'Ropa y calzado',
  'Cuidado personal',
  'Tecnología y electrónicos',
  'Suscripciones',
  'Internet y telefonía',
  'Hogar y muebles',
  'Mascotas',
  'Seguros',
  'Impuestos',
  'Deudas y préstamos',
  'Hijos y familia',
  'Deportes y gimnasio',
  'Viajes y turismo',
  'Mantenimiento de vehículo',
  'Regalos y donaciones',
  'Otros gastos',
  'Jubilación',
  'Inversión',
  'Negocio',
  'Hijos y familia',
  'Boda o evento',
  'Hogar y muebles',
  'Pago de deudas',
  'Mascotas',
];

describe('iconoDeCategoria', () => {
  it('devuelve un icono propio para las 56 categorias de la base de datos', () => {
    expect(CATEGORIAS_DE_LA_BD).toHaveLength(56);

    const sinIcono = CATEGORIAS_DE_LA_BD.filter(
      (nombre) => iconoDeCategoria(nombre) === ICONO_DEFECTO
    );

    // Deja ver en el mensaje de error cuales categorias quedaron sin icono.
    expect(sinIcono).toEqual([]);
  });

  it('siempre devuelve un icono del set mdi', () => {
    const noMdi = CATEGORIAS_DE_LA_BD.map((nombre) =>
      iconoDeCategoria(nombre)
    ).filter((icono) => !icono.startsWith('mdi:'));

    expect(noMdi).toEqual([]);
  });

  it('ignora mayusculas y tildes al buscar', () => {
    expect(iconoDeCategoria('ALIMENTACIÓN')).toBe('mdi:food');
    expect(iconoDeCategoria('  alimentacion  ')).toBe('mdi:food');
    expect(iconoDeCategoria('Tecnología y Electrónicos')).toBe('mdi:laptop');
  });

  it('conserva el icono de los nombres cortos guardados en el navegador', () => {
    expect(iconoDeCategoria('comida')).toBe('mdi:food');
    expect(iconoDeCategoria('gym')).toBe('mdi:dumbbell');
    expect(iconoDeCategoria('arriendo')).toBe('mdi:home-currency-usd');
  });

  it('usa el icono generico cuando la categoria es desconocida o vacia', () => {
    expect(iconoDeCategoria('Categoría inventada')).toBe(ICONO_DEFECTO);
    expect(iconoDeCategoria('')).toBe(ICONO_DEFECTO);
    expect(iconoDeCategoria()).toBe(ICONO_DEFECTO);
  });
});
