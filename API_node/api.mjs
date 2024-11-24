import express from 'express';
import axios from 'axios';
import csv from 'csv-parser';
import fs from 'fs';
import dotenv from 'dotenv';
import cors from 'cors';
dotenv.config();

const accionsPath = './DB/accions.csv';
const tramitsPath = './DB/tramits.csv';

const tramitColumns = ['Titol', 'Id', 'Vigent'];
const accioColumns = ['Tramit', 'Sessio'];

const app = express();

app.disable('x-powered-by');

app.use(cors());

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

app.use(express.json());

// Cohere API configuration
const COHERE_API_KEY = process.env.COHERE_API_KEY;
const COHERE_BASE_URL = 'https://api.cohere.ai';

app.post('/generate-description', async (req, res) => {
  const prompt = 'Genera una sinopsis de menys de 20 paraules del següent tràmit que podria fer una persona: ' + req.body.Titol;

  if (!prompt) {
    return res.status(400).json({ error: 'El campo "prompt" es obligatorio.' });
  }

  try {
    // Realizar la solicitud a la API de Cohere
    const response = await axios.post(
        `${COHERE_BASE_URL}/generate`,
        {
          model: 'command-xlarge-nightly', // Modelo, ajusta según tus necesidades
          prompt,
          max_tokens: 100, // Valor predeterminado si no se especifica
          temperature: 0.7
        },
        {
          headers: {
            Authorization: `Bearer ${COHERE_API_KEY}`,
            'Content-Type': 'application/json'
          }
        }
    );

    // Devolver la respuesta al cliente
    res.json(response.data.text);
  } catch (error) {
    console.error('Error al consumir la API de Cohere:', error.response?.data || error.message);
    res.status(500).json({ error: 'Error while processing the prompt' });
  }
});

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
  const sessio = accions.get(id).Sessio;
  const tramit = accions.get(id).Tramit;
  const encodedSessio = sessio.replace(/ /g, '%20').replace(/\//g, '%2F');
  const encodedTramit = tramit.replace(/ /g, '%20').replace(/\//g, '%2F');

  try {
    const response = await axios.get(`${API_AI}/${encodedSessio}/${encodedTramit}`);
    const result = [];
    for (let i = 0; i < response.data.length; ++i) {
      if (response.data[i].Vigent) {
        const recomm = response.data[i];
        try {
          const descriptionResponse = await axios.post(`${BASE_URL}/generate-description`, { Titol: recomm.Titol });
          recomm.Descripcio = descriptionResponse.data;
        } catch (err) {
          throw new Error('Error fetching description: ' + err.message);
        }
        result.push(recomm);
      }
    }
    if (result.length > 0) {
      console.log('Returning recommendations:', result);
      return result;
    }
    if (response.data.length === 0) throw new Error('No recommendations found');
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
