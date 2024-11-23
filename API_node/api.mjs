import express from 'express';

const app = express();

app.disable('x-powered-by');

const PORT = process.env.PORT ?? 3000;

app.listen(PORT, () => {
  console.log(`Server listening port http://localhost:${PORT}`);
});
