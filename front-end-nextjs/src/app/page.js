'use client';

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [url, setUrl] = useState('');
  const [qrCodeUrl, setQrCodeUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!url) {
      setError('Podaj URL');
      return;
    }

    setError('');
    setQrCodeUrl('');
    setLoading(true);

    try {
      // wysyłamy POST na backend, url jako query param
      const response = await axios.post(
        'http://localhost:8000/generate-qr/',
        null,
        {
          params: { url }, // ?url=...
        }
      );

      setQrCodeUrl(response.data.qr_code_url);
    } catch (err) {
      console.error('Error generating QR Code:', err);
      setError('Nie udało się wygenerować kodu QR');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>QR Code Generator</h1>

      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL like https://example.com"
          style={styles.input}
        />
        <button
          type="submit"
          style={styles.button}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate QR Code'}
        </button>
      </form>

      {error && (
        <p style={{ color: 'tomato', marginTop: '10px' }}>
          {error}
        </p>
      )}

      {qrCodeUrl && (
        <img
          src={qrCodeUrl}
          alt="QR Code"
          style={styles.qrCode}
        />
      )}
    </div>
  );
}

// Styles (zwykły JS object)
const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#121212',
    color: 'white',
  },
  title: {
    margin: 0,
    lineHeight: '1.15',
    fontSize: '4rem',
    textAlign: 'center',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  input: {
    padding: '10px',
    borderRadius: '5px',
    border: 'none',
    marginTop: '20px',
    width: '300px',
    color: '#121212',
  },
  button: {
    padding: '10px 20px',
    marginTop: '20px',
    border: 'none',
    borderRadius: '5px',
    backgroundColor: '#0070f3',
    color: 'white',
    cursor: 'pointer',
  },
  qrCode: {
    marginTop: '20px',
    maxWidth: '300px',
  },
};
