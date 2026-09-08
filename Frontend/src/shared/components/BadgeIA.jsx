import React from 'react';
import './BadgeIA.css';

const BadgeIA = ({ mini = false }) => (
  <span className={`badge-ia-chat${mini ? ' badge-ia-chat--mini' : ''}`}>
    <span className="badge-ia-chat__punto" />
    IA
  </span>
);

export default BadgeIA;