import React from 'react';
import { formatearMensajeIA } from '../../core/utils/formatearMensajeIA';
import './MensajeIA.css';

const MensajeIA = ({ texto }) => <>{formatearMensajeIA(texto)}</>;

export default MensajeIA;