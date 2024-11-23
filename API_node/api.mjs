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
const API_IA = 'http://alberto/recommendations';

app.get('/', (req, res) => {
  res.status(200).json({ message: 'API en ejecución' });
});

async function getRecommendations (id) {
  const tramit = accions.get(id).Tramit;
  const sessio = accions.get(id).Sessio;
  const encodedTramit = encodeURIComponent(tramit);
  const encodedSessio = encodeURIComponent(sessio);

  try {
    const response = await axios.get(`${API_IA}/${encodedTramit}/${encodedSessio}`);
    for (let i = 0; i < response.data.length; ++i) {
      if (response.data[i].vigent) return response.data;
    }
    return await getRecommendations(response.data.id);
  } catch (error) {
    throw new Error('Error fetching recommendations: ' + error.message);
  }
}

app.get('/recommendation/:title', async (req, res) => {
  const title = req.params.title;
  const id = tramits.get(title).Id;
  getRecommendations(id)
    .then(rec => res.json(rec))
    .catch(err => res.status(500).json({ error: err.message }));
});

app.use((req, res) => {
  res.status(404).send('<h1>404 - Página no encontrada</h1>');
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${BASE_URL}`);
});

// app.get('/recommendations/*', async (req, res) => {
//   const title = req.url.split('/')[2];
//   const tramit = tramits.get(title);
//   if (!tramit) {
//     return res.status(404).json({ error: 'Tramit not found' });
//   }
//   const accio = accions.get(tramit.Id);
//   if (!accio) {
//     return res.status(404).json({ error: 'Accio not found' });
//   }
//   const requestData = {
//     Titol: tramit.Titol,
//     Sessio: accio.Sessio
//   };
//   try {
//     console.log(requestData);
//     const recommendations = await getRecommendations(requestData);
//     res.json(recommendations);
//   } catch (err) {
//     res.status(500).json({ error: err.message });
//   }
// });
