/**
 * Kompresor – Vizualizácia prietoku a rosného bodu
 *
 * Tento React komponent slúži na vizualizáciu údajov zo senzorov merajúcich prietok vzduchu (v m³/h)
 * a rosného bodu (v °C) v rôznych častiach systému. Údaje sú získavané z backend API a zobrazované
 * vo forme prehľadných kariet a interaktívneho grafu.
 *
 * Funkcie komponentu:
 * - Načítanie aktuálnych hodnôt zo senzorov pri načítaní komponentu.
 * - Kliknutím na ktorúkoľvek kartu senzora sa otvorí modálne okno s historickým grafom.
 * - Graf podporuje zoom/pan, výber časového rozsahu a export údajov do CSV.
 * - Zobrazovanie výpadkov spojenia medzi meraniami pomocou prerušenej červenej línie.
 * - Reaktívne zobrazenie s prispôsobením farieb a jednotiek pre jednotlivé senzory.
 */


// Import potrebných knižníc a komponentov
import React, { useEffect, useState, useRef } from 'react';
import './compressor.css';
import axios from 'axios';
import Modal from 'react-modal';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  TimeScale,
  Tooltip,
  Legend,
  Filler,
  Title
} from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import 'chartjs-adapter-date-fns';

// Registrácia modulov pre Chart.js
ChartJS.register(
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  TimeScale,
  Tooltip,
  Legend,
  Filler,
  Title,
  zoomPlugin
);

// Nastavenie modálneho okna na koreňový element
Modal.setAppElement('#root');

const Compressor = () => {
  // Hooky na ukladanie stavu
  const [timeRange, setTimeRange] = useState('7d'); // Predvolený rozsah pre graf
  const [sensorData, setSensorData] = useState([]); // Aktuálne hodnoty zo senzorov
  const [modalIsOpen, setModalIsOpen] = useState(false); // Stav modálneho okna
  const [selectedSensor, setSelectedSensor] = useState(null); // Aktuálne zvolený senzor pre detail
  const [historyData, setHistoryData] = useState([]); // Historické dáta pre graf
  const chartRef = useRef(); // Ref na objekt grafu

  // Zoznam senzorov s popisom a jednotkami
  const sensorLabels = [
    { key: 'flowVolume_01', label: 'Hlavný výstup', unit: 'm³/h' },
    { key: 'flowVolume_02', label: 'Rozvodňa 22kV', unit: 'm³/h' },
    { key: 'flowVolume_03', label: 'EOP 24A', unit: 'm³/h' },
    { key: 'flowVolume_04', label: 'Výrobná hala', unit: 'm³/h' },
    { key: 'flowVolume_05', label: 'FJ24 - REZ', unit: 'm³/h' },
    { key: 'flowVolume_06', label: 'FJ Odpich', unit: 'm³/h' },
    { key: 'flowVolume_07', label: 'Vykládka Zavážanie', unit: 'm³/h' },
    { key: 'flowVolume_08', label: 'FJ24 - 24B', unit: 'm³/h' },
    { key: 'dewPoint_01', label: 'Rosný bod', unit: '°C' },
  ];

  const apiBaseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Načítanie najnovších údajov zo senzorov pri načítaní komponentu
  useEffect(() => {
    const fetchData = () => {
      axios.get(`${apiBaseUrl}/api/latest/`)
        .then(response => setSensorData(response.data))
        .catch(error => console.error('Chyba pri načítaní senzorov:', error));
    };
  
    fetchData(); // okamžité načítanie
    const interval = setInterval(fetchData, 10000); // každých 10 sekúnd
  
    return () => clearInterval(interval); // vyčistenie pri odpojení komponentu
  }, [apiBaseUrl]);
  

  // Otvorenie modálneho okna a načítanie historických dát pre vybraný senzor
  const openModal = (sensorKey) => {
    setSelectedSensor(sensorKey);
    setModalIsOpen(true);
    axios.get(`${apiBaseUrl}/api/history/${sensorKey}/`)
      .then(response => setHistoryData(response.data))
      .catch(err => console.error('Chyba pri načítaní historických dát:', err));
  };

  // Zavretie modálneho okna a reset vybraných dát
  const closeModal = () => {
    setModalIsOpen(false);
    setSelectedSensor(null);
    setHistoryData([]);
  };

  // Získanie hodnoty senzora podľa jeho kľúča
  const getSensorValue = (key) => {
    const item = sensorData.find(s => s.sensor === key);
    return item ? item.value.toFixed(1) : '–';
  };

  // Získanie popisu senzora
  const getSensorLabel = (key) =>
    sensorLabels.find(s => s.key === key)?.label || key;

  // Získanie jednotky senzora
  const getSensorUnit = (key) =>
    sensorLabels.find(s => s.key === key)?.unit || '';

  // Vytvorenie dátového objektu pre graf vrátane detekcie výpadkov spojenia
  const getChartData = () => {
    const dataset = historyData.map(d => ({
      x: new Date(d.timestamp),
      y: d.value
    }));

    return {
      datasets: [
        {
          label: `${getSensorLabel(selectedSensor)} (${getSensorUnit(selectedSensor)})`,
          data: dataset,
          borderColor: '#00bcd4',
          backgroundColor: 'rgba(0,188,212,0.1)',
          tension: 0.3,
          pointRadius: 0,
          fill: true,
          spanGaps: false,
          segment: {
            // Detekcia výpadku - prerušovaná čiara ak rozdiel medzi bodmi > 10 minút
            borderDash: ctx => {
              if (!ctx || !ctx.p0 || !ctx.p1) return;
              const prev = ctx.p0.parsed;
              const curr = ctx.p1.parsed;
              const diff = (curr.x - prev.x) / 60000;
              return diff > 10 ? [6, 6] : undefined;
            },
            borderColor: ctx => {
              if (!ctx || !ctx.p0 || !ctx.p1) return '#00bcd4';
              const prev = ctx.p0.parsed;
              const curr = ctx.p1.parsed;
              const diff = (curr.x - prev.x) / 60000;
              return diff > 10 ? 'red' : '#00bcd4';
            }
          }
        },
        {
          // Dummy dataset pre označenie výpadku
          label: 'Výpadok spojenia',
          data: [{ x: new Date(), y: null }],
          borderColor: 'red',
          borderDash: [6, 6],
          pointRadius: 0,
          borderWidth: 2,
          fill: false,
          hidden: false,
          showLine: true
        }
      ]
    };
  };

  const chartData = getChartData();

  // Konfigurácia možností zobrazenia grafu
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: '#333',
        titleColor: '#00bcd4',
        bodyColor: '#eee',
        titleFont: { weight: 'bold' },
        callbacks: {
          label: (context) => {
            const value = context.parsed.y;
            const unit = getSensorUnit(selectedSensor);
            return ` ${value} ${unit}`;
          }
        }
      },
      zoom: {
        pan: { enabled: true, mode: 'x' },
        zoom: {
          wheel: { enabled: true },
          pinch: { enabled: true },
          mode: 'x'
        }
      }
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'hour',
          stepSize: 2,
          displayFormats: { hour: 'HH:mm' },
          tooltipFormat: 'HH:mm'
        },
        // Výpočet minimálneho času podľa zvoleného rozsahu
        min: (() => {
          const now = Date.now();
          switch (timeRange) {
            case '6h': return new Date(now - 6 * 60 * 60 * 1000);
            case '12h': return new Date(now - 12 * 60 * 60 * 1000);
            case '24h': return new Date(now - 24 * 60 * 60 * 1000);
            case '48h': return new Date(now - 48 * 60 * 60 * 1000);
            case '7d': return new Date(now - 7 * 24 * 60 * 60 * 1000);
            default: return new Date(now - 24 * 60 * 60 * 1000);
          }
        })(),
        max: new Date(),
        ticks: {
          color: 'white',
          maxTicksLimit: 12,
          stepSize: 2
        },
        title: { display: true, text: 'Čas' },
        grid: { color: 'rgba(255,255,255,0.1)' }
      },
      y: {
        beginAtZero: false,
        title: { display: true, text: getSensorUnit(selectedSensor) },
        ticks: { color: 'white' },
        grid: { color: 'rgba(255,255,255,0.1)' }
      }
    }
  };

  // Funkcia na exportovanie historických dát do CSV súboru
  const exportCSV = () => {
    if (!historyData.length) return;

    const csvContent = 'timestamp,value\n' +
      historyData.map(d => `${d.timestamp},${d.value}`).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${selectedSensor}_data.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Resetovanie priblíženia grafu
  const resetZoom = () => {
    chartRef.current?.resetZoom();
  };

  // Renderovanie komponentu
  return (
    <div className="dashboard-container">
      <h2>💨 Prietok vzduchu v potrubí | 💧 Rosný bod</h2>

      {/* Zobrazenie kariet senzorov */}
      <div className="sensor-grid">
        {sensorLabels.map((sensor, idx) => (
          <div key={idx} className="sensor-box" onClick={() => openModal(sensor.key)}>
            <h3>{sensor.label}</h3>
            <div className="sensor-value">{getSensorValue(sensor.key)}</div>
            <div>{sensor.unit}</div>
          </div>
        ))}
      </div>

      {/* Modálne okno s grafom */}
      <Modal isOpen={modalIsOpen} onRequestClose={closeModal} contentLabel="Graf senzorov" className="chart-modal">
        <h2>{getSensorLabel(selectedSensor)}</h2>
        <Line data={chartData} options={chartOptions} ref={chartRef} />
        <div className="chart-buttons">
          <select onChange={(e) => setTimeRange(e.target.value)} defaultValue="7d">
            <option value="6h">Posledných 6h</option>
            <option value="12h">Posledných 12h</option>
            <option value="24h">Posledných 24h</option>
            <option value="48h">Posledných 48h</option>
            <option value="7d">Posledných 7 dní</option>
          </select>
          <button onClick={resetZoom}>Resetovať graf</button>
          <button onClick={exportCSV}>Exportovať CSV</button>
          <button onClick={closeModal}>Zavrieť</button>
        </div>
      </Modal>
    </div>
  );
};

export default Compressor;
