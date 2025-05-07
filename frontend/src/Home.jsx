/**
 * Home.jsx – Úvodná obrazovka SCADA systému OFZ
 *
 * Tento komponent zobrazuje uvítaciu stránku pre webovú aplikáciu SCADA systému spoločnosti OFZ, a.s.
 * Obsahuje logo, názov systému a uvítací text s inštrukciou na výber aplikácie z menu.
 * Používateľsky prívetivý dizajn s centrickým zarovnaním a kontrastným štýlom vhodným pre priemyselné použitie.
 */

import React from 'react';

const Home = () => {
  return (
    <div style={{
      padding: '30px',
      fontFamily: 'Arial, sans-serif',
      color: '#eee',
      background: '#1b1b1b',
      minHeight: '100vh',
      textAlign: 'center',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <h1 style={{ marginBottom: '30px', fontSize: '32px' }}>
        🏭 OFZ SCADA 🏭
      </h1>

      <img 
        src="/assets/logo_ofz.png" 
        alt="Logo OFZ" 
        style={{ 
          width: '250px',
          height: '250px',
          objectFit: 'contain',
          marginBottom: '30px',
          borderRadius: '30px',
          boxShadow: '0 0 30px rgba(0, 0, 0, 0.6)',
          backgroundColor: 'white',
          padding: '20px'
        }}
      />

      <p style={{ fontSize: '18px', maxWidth: '500px', color: '#ccc' }}>
        Vitajte v SCADA systéme OFZ, a.s.  
        <br />Vyberte si aplikáciu z menu vyššie.
      </p>
    </div>
  );
};

export default Home;
