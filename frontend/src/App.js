/**
 * App.js – Hlavná aplikácia SCADA rozhrania
 *
 * Tento komponent slúži ako hlavný kontajner pre celú React aplikáciu. Zabezpečuje navigáciu medzi jednotlivými
 * podstránkami pomocou React Router. Obsahuje hlavnú navigačnú lištu (menu) s odkazmi na úvodnú stránku a vizualizáciu
 * kompresorovej stanice. Definuje aj základný štýl pozadia a interakcie s odkazmi (hover efekt).
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './Home';
import Compressor from './Compressor';

// Štýl pre odkazy v navigácii
const navLinkStyle = {
  color: '#eee',
  marginRight: '20px',
  textDecoration: 'none',
  fontSize: '18px',
  transition: 'color 0.4s, transform 0.4s, text-shadow 0.4s'
};

// Zvýraznenie odkazu pri prechode myšou
const handleMouseOver = (e) => {
  e.target.style.color = '#00bcd4';
  e.target.style.transform = 'scale(1.08)';
  e.target.style.textShadow = '0 0 10px #00bcd4, 0 0 20px #00bcd4';
};

// Obnovenie pôvodného štýlu odkazu pri opustení myšou
const handleMouseOut = (e) => {
  e.target.style.color = '#eee';
  e.target.style.transform = 'scale(1)';
  e.target.style.textShadow = 'none';
};

// Hlavný komponent aplikácie
function App() {
  return (
    <Router>
      {/* Obal aplikácie so základným pozadím */}
      <div style={{ background: '#1b1b1b', minHeight: '100vh', fontFamily: 'Arial' }}>
        
        {/* Navigačná lišta */}
        <nav style={{
          backgroundColor: '#1b1b1b',
          padding: '10px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-start',
          borderBottom: '2px solid #333'
        }}>
          {/* Odkaz na domovskú stránku */}
          <Link
            to="/"
            style={{ ...navLinkStyle, fontSize: '24px', marginRight: '40px' }}
            onMouseOver={handleMouseOver}
            onMouseOut={handleMouseOut}
          >
            🏭 OFZ SCADA 🏭
          </Link>

          {/* Odkaz na kompresorovú stanicu */}
          <Link
            to="/compressor"
            style={navLinkStyle}
            onMouseOver={handleMouseOver}
            onMouseOut={handleMouseOut}
          >
            Kompresorová stanica
          </Link>
        </nav>

        {/* Definovanie jednotlivých stránok podľa cesty */}
        <Routes>
          <Route path="/" element={<Home />} />               {/* Úvodná stránka */}
          <Route path="/compressor" element={<Compressor />} /> {/* Vizualizácia kompresorov */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
