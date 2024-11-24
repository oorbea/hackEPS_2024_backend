# hackEPS_2024_backend
## Hola! Aquí t'ensenyem a aixecar les apis!

## Com aixecar l'API de Node.js

Per aixecar l'API, segueix els següents passos (contant que ja has instal·lat Node.js i npm prèviament):

1. Clona el repositori:
    ```bash
    git clone https://github.com/oorbea/hackEPS_2024_backend
    ```

2. Entra al directori del projecte:
    ```bash
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

## Com aixecar l'API de Flask

Per aixecar l'API, segueix els següents passos (contant que ja has instal·lat Python i pip prèviament):

1. Clona el repositori:
    ```bash
    git clone https://github.com/oorbea/hackEPS_2024_backend
    ```

2. Entra al directori del projecte:
    ```bash
    cd API_flask
    ```

3. Crea un entorn virtual:
    ```bash
    python -m venv venv
    ```

4. Activa l'entorn virtual:
    - A Windows:
        ```bash
        venv\Scripts\activate
        ```
    - A macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. Instal·la les dependències:
    ```bash
    pip install -r requirements.txt
    ```

6. Descarrega la base de dades i situa-la a hackEPS_2024_backend\API_flask\data

7. Executa preprocesado1:
    ```bash
    cd utils
    python preprocesado1.py
    ```

8. Executa l'API:
    ```bash
    cd ..
    python main.py
    ```

L'API estarà disponible a `http://localhost:500`.