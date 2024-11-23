import express from 'express';
import axios from 'axios';
import csv from 'csv-parser';
import fs from 'fs';
import dotenv from 'dotenv';
dotenv.config();

const accionsPath = './DB/accions.csv';
const tramitsPath = './DB/tramits.csv';

const tramitColumns = ['Titol', 'Id', 'Vigent'];
const accioColumns = ['Tramit', 'Sessio'];

const tramits = new Map();

// Read tramits.csv and store the data in a Map
fs.createReadStream(tramitsPath)
  .pipe(csv())
  .on('data', (row) => {
    const tramit = {};
    tramitColumns.forEach((column) => {
      if (row[column] !== undefined) {
        if (row[column] === 'True') tramit[column] = true;
        else if (row[column] === 'False') tramit[column] = false;
        else tramit[column] = row[column];
      }
    });
    tramits.set(row.Titol, tramit);
  })
  .on('end', () => {
    console.log('CSV file read.');
  })
  .on('error', (err) => {
    console.error('Error reading the file:' + err);
  });

const accions = new Map();

// Read accions.csv and store the data in a Map
fs.createReadStream(accionsPath)
  .pipe(csv())
  .on('data', (row) => {
    const accio = {};
    accioColumns.forEach((column) => {
      if (row[column] !== undefined) {
        accio[column] = row[column];
      }
    });
    accions.set(row.Tramit, accio);
  })
  .on('end', () => {
    console.log('Accions CSV file read.');
  })
  .on('error', (err) => {
    console.error('Error reading the accions file:' + err);
  });

const app = express();

app.disable('x-powered-by');

const PORT = process.env.PORT ?? 3000;
const BASE_URL = `http://localhost:${PORT}`;
const API_AI = 'http://localhost:5000/predict';

app.get('/', (req, res) => {
  res.status(200).json({ message: 'API running' });
});

/**
 * Fetches recommendations based on the provided ID.
 *
 * This function retrieves the 'Tramit' and 'Sessio' values associated with the given ID,
 * encodes them, and makes a request to an external API to get recommendations. If the
 * recommendations contain a valid entry, it returns the data. Otherwise, it recursively
 * fetches recommendations based on the last entry's ID.
 *
 * @param {string} id - The ID used to fetch 'Tramit' and 'Sessio' values.
 * @returns {Promise<Object[]>} - A promise that resolves to an array of recommendation objects.
 * @throws {Error} - Throws an error if the request to the external API fails.
 */
async function getRecommendations (id) {
  const tramit = accions.get(id).Tramit;
  const sessio = accions.get(id).Sessio;
  const encodedTramit = encodeURIComponent(tramit);
  const encodedSessio = encodeURIComponent(sessio);

  try {
    const response = await axios.get(`${API_AI}/${encodedSessio}/${encodedTramit}`);
    for (let i = 0; i < response.data.length; ++i) {
      if (response.data[i].vigent) return response.data;
    }
    return await getRecommendations(response.data[response.data.length - 1].id);
  } catch (error) {
    throw new Error('Error fetching recommendations: ' + error.message);
  }
}

// Method to get the recommendations for a given title
app.get('/recommendation/:title', async (req, res) => {
  const title = req.params.title;
  const id = tramits.get(title).Id;
  getRecommendations(id)
    .then(rec => res.json(rec))
    .catch(err => res.status(500).json({ error: err.message }));
});

// In case the route is not found
app.use((req, res) => {
  res.status(404).send('<h1>404 - Página no encontrada</h1>');
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${BASE_URL}`);
});
