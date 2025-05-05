import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './Home';
import Compressor from './Compressor';

const navLinkStyle = {
  color: '#eee',
  marginRight: '20px',
  textDecoration: 'none',
  fontSize: '18px',
  transition: 'color 0.4s, transform 0.4s, text-shadow 0.4s'
};

const handleMouseOver = (e) => {
  e.target.style.color = '#00bcd4';
  e.target.style.transform = 'scale(1.08)';
  e.target.style.textShadow = '0 0 10px #00bcd4, 0 0 20px #00bcd4';
};

const handleMouseOut = (e) => {
  e.target.style.color = '#eee';
  e.target.style.transform = 'scale(1)';
  e.target.style.textShadow = 'none';
};

function App() {
  return (
    <Router>
      <div style={{ background: '#1b1b1b', minHeight: '100vh', fontFamily: 'Arial' }}>
        <nav style={{
          backgroundColor: '#1b1b1b',
          padding: '10px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-start',
          borderBottom: '2px solid #333'
        }}>
          <Link
            to="/"
            style={{ ...navLinkStyle, fontSize: '24px', marginRight: '40px' }}
            onMouseOver={handleMouseOver}
            onMouseOut={handleMouseOut}
          >
            🏭 OFZ SCADA 🏭
          </Link>

          <Link
            to="/compressor"
            style={navLinkStyle}
            onMouseOver={handleMouseOver}
            onMouseOut={handleMouseOut}
          >
            Kompresorová stanica
          </Link>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/compressor" element={<Compressor />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
