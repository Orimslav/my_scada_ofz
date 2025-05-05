import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Compressor() {
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/latest/')
      .then(response => {
        setSensorData(response.data);
      })
      .catch(error => {
        console.error('Chyba pri načítaní senzorov:', error);
      });
  }, []);

  return (
    <div>
      <h2>Kompresorová stanica – aktuálne hodnoty</h2>
      <pre>{JSON.stringify(sensorData, null, 2)}</pre>
    </div>
  );
}

export default Compressor;
