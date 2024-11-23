import express from 'express';
import axios from 'axios';
import csv from 'csv-parser';
import fs from 'fs';
import dotenv from 'dotenv';
dotenv.config();

const accionsPath = './DB/accions.csv';
const tramitsPath = './DB/tramits.csv';

const app = express();

app.disable('x-powered-by');

const PORT = process.env.PORT ?? 3000;
const BASE_URL = `http://localhost:${PORT}`;
const API_IA = 'http://alberto/recommendations';

app.get('/', (req, res) => {
  res.status(200).json({ message: 'API en ejecución' });
});

async function getRecommendations (title) {
  try {
    const response = await axios.get(`${API_IA}/${title}`);
    for (let i = 0; i < response.data.length; ++i) {
      if (response.data[i].vigent) return response.data;
    }
    return await getRecommendations(response.data.title);
  } catch (error) {
    throw new Error('Error fetching recommendations: ' + error.message);
  }
}

app.get('/recommendation/*', async (req, res) => {
  const title = req.url.split('/')[2];
  getRecommendations(title)
    .then(rec => res.json(rec))
    .catch(err => res.status(500).json({ error: err.message }));
});

app.use((req, res) => {
  res.status(404).send('<h1>404 - Página no encontrada</h1>');
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${BASE_URL}`);
});
