# hackEPS_2024_backend
## Com aixecar l'API

Per aixecar l'API, segueix els següents passos:

1. Clona el repositori:
    ```bash
    git clone https://github.com/oorbea/hackEPS_2024_backend
    ```

2. Entra al directori del projecte:
    ```bash
    cd hackEPS_2024_backend
    cd API_node
    ```

3. Instal·la les dependències:
    ```bash
    npm install --only=production
    ```

4. Descarrega la base de dades i situa-la a hackEPS_2024_backend\BD

5. Configura les variables d'entorn:
    Crea un fitxer `.env` a la arrel del projecte amb les següents variables:
    ```
    PORT={port que desitgis}
    ```

6. Executa l'API:
    ```bash
    npm run start
    ```

L'API estarà disponible a `http://localhost:{PORT}`.