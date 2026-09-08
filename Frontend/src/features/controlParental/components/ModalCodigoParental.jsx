import React, { useState } from 'react';

const ModalCodigoParental = ({
  titulo,
  descripcion,
  abierto,
  cargando,
  onConfirmar,
  onCerrar,
}) => {
  const [codigo, setCodigo] = useState('');

  if (!abierto) {
    return null;
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (codigo.length !== 6) {
      return;
    }

    const confirmado = await onConfirmar(codigo);

    if (confirmado) {
      setCodigo('');
    }
  };

  return (
    <div className="modal-parental-fondo">
      <form
        className="modal-parental"
        onSubmit={handleSubmit}
      >
        <h2>{titulo}</h2>

        <p>{descripcion}</p>

        <input
          type="text"
          inputMode="numeric"
          maxLength="6"
          pattern="[0-9]{6}"
          value={codigo}
          onChange={(event) => {
            const valor = event.target.value
              .replace(/\D/g, '')
              .slice(0, 6);

            setCodigo(valor);
          }}
          placeholder="000000"
          required
        />

        <div>
          <button
            type="button"
            onClick={onCerrar}
          >
            Cancelar
          </button>

          <button
            type="submit"
            disabled={cargando || codigo.length !== 6}
          >
            {cargando ? 'Validando...' : 'Confirmar'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ModalCodigoParental;
