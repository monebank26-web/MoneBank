import { useState } from 'react';

export const useModalesBolsillos = ({ eliminar }) => {
  const [modalCrearAbierto, setModalCrearAbierto] = useState(false);
  const [bolsilloParaDepositar, setBolsilloParaDepositar] = useState(null);
  const [modalTransferirAbierto, setModalTransferirAbierto] = useState(false);
  const [bolsilloParaEditar, setBolsilloParaEditar] = useState(null);
  const [bolsilloOrigenTransferencia, setBolsilloOrigenTransferencia] = useState(null);
  const [bolsilloParaEliminar, setBolsilloParaEliminar] = useState(null);

  const abrirTransferir = (bolsillo = null) => {
    setBolsilloOrigenTransferencia(bolsillo);
    setModalTransferirAbierto(true);
  };

  const cerrarTransferir = () => {
    setModalTransferirAbierto(false);
    setBolsilloOrigenTransferencia(null);
  };

  const confirmarEliminar = async () => {
    await eliminar(bolsilloParaEliminar.id);
    setBolsilloParaEliminar(null);
  };

  return {
    modalCrearAbierto,
    setModalCrearAbierto,
    bolsilloParaDepositar,
    setBolsilloParaDepositar,
    modalTransferirAbierto,
    bolsilloParaEditar,
    setBolsilloParaEditar,
    bolsilloOrigenTransferencia,
    bolsilloParaEliminar,
    setBolsilloParaEliminar,
    abrirTransferir,
    cerrarTransferir,
    confirmarEliminar,
  };
};
