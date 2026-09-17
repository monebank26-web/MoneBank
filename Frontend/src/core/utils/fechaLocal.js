const dosDigitos = (n) => String(n).padStart(2, '0');

export const fechaLocalHoy = () => {
  const ahora = new Date();
  return `${ahora.getFullYear()}-${dosDigitos(ahora.getMonth() + 1)}-${dosDigitos(ahora.getDate())}`;
};

export const fechaHoraLocalHoy = () => {
  const ahora = new Date();
  return (
    `${ahora.getFullYear()}-${dosDigitos(ahora.getMonth() + 1)}-${dosDigitos(ahora.getDate())}` +
    `T${dosDigitos(ahora.getHours())}:${dosDigitos(ahora.getMinutes())}:${dosDigitos(ahora.getSeconds())}`
  );
};