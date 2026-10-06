# DEVLOG — InternScout

Bitácora de construcción del proyecto: qué se hizo, en qué orden, y por qué. Se actualiza a medida que avanzamos (no depende de los commits — es un registro aparte).

---

## 2026-09-16

### 1. Estructura inicial del proyecto (MVP — Fase 1)

Se creó solo el subconjunto de carpetas necesario para el MVP (fetch → normalize → guardar en Mongo → notificar por Telegram), evitando andamiaje para fases futuras (Adzuna, Karriere.at, Stepstone, filtros, GitHub Actions):

```
src/
├── __init__.py
├── main.py
├── config.py
├── collectors/
│   ├── __init__.py
│   └── arbeitnow.py
├── processing/
│   ├── __init__.py
│   └── normalizer.py
├── db/
│   ├── __init__.py
│   ├── mongo_client.py
│   └── repository.py
└── notifier/
    ├── __init__.py
    └── telegram_bot.py
```

`tests/` se creará cuando escribamos el primer test, no antes. La clase abstracta `collectors/base.py` se agregará en la Fase 2, cuando exista un segundo collector real que la necesite.

### 2. `pyproject.toml`

Dependencias declaradas: `pymongo`, `python-telegram-bot`, `requests`, `beautifulsoup4`, `python-dotenv`, `pytest`.

Se configuró `[build-system]` (setuptools) + `[tool.setuptools.packages.find]` con `include = ["src*"]` para poder instalar el proyecto en modo editable (`pip install -e .`) y que `src` y sus subpaquetes sean importables desde cualquier lado.

### 3. Entorno virtual

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

Instalación verificada — todas las dependencias se resolvieron correctamente.

### 4. MongoDB Atlas — cuenta, cluster y credenciales

Cuenta creada en MongoDB Atlas. Cluster gratuito M0 (`Cluster0`) creado: AWS, región `us-east-1` (N. Virginia). Se usó "Automate security setup" (sin dataset de ejemplo) para generar automáticamente el usuario de base de datos y agregar la IP local a la whitelist de acceso.

`MONGO_URI` obtenido desde Atlas → Connect → Drivers → Python (connection string `mongodb+srv://...`).

Nota: la whitelist de IP solo incluye la IP local por ahora. Cuando lleguemos a la Fase 4 (automatización con GitHub Actions), habrá que ampliarla.

### 5. Bot de Telegram

Bot creado vía @BotFather (`/newbot`) → `@InternScoutSergio_bot`, con su `TELEGRAM_BOT_TOKEN`.

`TELEGRAM_CHAT_ID` obtenido enviando `/start` + un mensaje al bot y leyendo el campo `chat.id` desde `https://api.telegram.org/bot<TOKEN>/getUpdates`.

### 6. Variables de entorno

Se creó `.env.example` (plantilla, sin valores reales — sí se sube a git) con `MONGO_URI`, `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`. Se creó `.env` local con los valores reales, y se verificó con `git status` que no aparece como untracked (el `.gitignore` ya lo excluía correctamente).

**Fase 0 completa.**

### 7. MVP end-to-end (Fase 1) — Arbeitnow

Se implementó el pipeline completo, probando cada pieza con datos/credenciales reales antes de pasar a la siguiente:

- `src/config.py` — carga `MONGO_URI`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` desde `.env`. Probado: las 3 variables se leen correctamente.
- `src/collectors/arbeitnow.py` — `fetch_jobs()` trae la página 1 (250 ofertas) de la API pública. Probado con la API real.
- `src/processing/normalizer.py` — `normalize_arbeitnow_job()` calcula `job_hash` (sha256 de título+empresa+url, para dedup), limpia el HTML de la descripción con BeautifulSoup (snippet de 300 caracteres), y convierte `created_at` a fecha. Se dejaron fuera del MVP los campos `region_tag`, `role_type`, `sponsorship_flag` del modelo de datos original (son de la Fase 3) — Mongo no exige esquema fijo, se agregan después sin migrar nada.
- `src/db/mongo_client.py` — conecta a Atlas, base de datos `internscout`, colección `jobs`, con índice único sobre `job_hash`. Probado con ping real a Atlas.
- `src/db/repository.py` — `insert_if_new()` (usa `DuplicateKeyError` del índice único para detectar duplicados) y `mark_notified()`. Probado con un doc de prueba (insertado, duplicado, marcado, y borrado).
- `src/notifier/telegram_bot.py` — `send_job_notification()` usa `python-telegram-bot` (API async, envuelta con `asyncio.run()`). Probado con un mensaje real recibido en Telegram.
- `src/main.py` — orquestador `run(seed: bool)`. La bandera `--seed` guarda los jobs sin notificar, pensada para evitar una "avalancha" de mensajes al agregar una fuente nueva (aplica también a futuras fuentes en la Fase 2).

**Corrida real:** `python -m src.main --seed` sembró las 250 ofertas actuales sin notificar. Una segunda corrida `python -m src.main` (sin `--seed`) confirmó **0 nuevos / 0 mensajes**, probando que la deduplicación funciona correctamente de punta a punta.

**MVP (Fase 1) completo y validado.**

### 8. Automatización con GitHub Actions (Fase 4)

Se creó `.github/workflows/scrape.yml`: corre `python -m src.main` cada 6 horas (`0 */6 * * *`) más disparo manual (`workflow_dispatch`). Configuración manual (fuera del repo):
- GitHub Secrets: `MONGO_URI`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- Atlas Network Access: se agregó `0.0.0.0/0` (los runners de GitHub Actions no tienen IP fija)

### 9. Bug: "Event loop is closed" en notificaciones múltiples

La primera corrida manual del workflow falló (`exit code 1`, `Event loop is closed`). Causa: en `telegram_bot.py` se creaba un único `Bot` a nivel de módulo, y cada llamada a `send_job_notification()` usaba `asyncio.run()` — que crea y cierra un event loop nuevo cada vez. Al reusar el mismo `Bot` (con su cliente HTTP interno atado al primer event loop) en una segunda llamada dentro del mismo proceso, la conexión ya estaba cerrada.

No se detectó en las pruebas locales porque cada prueba mandaba un solo mensaje en un proceso nuevo — nunca se probó mandar 2+ mensajes seguidos en la misma ejecución, que es justo lo que pasa en producción cuando hay varias ofertas nuevas a la vez.

**Fix:** crear el `Bot` dentro de cada llamada con `async with Bot(...) as bot:`, para que el cliente HTTP se inicialice y cierre correctamente dentro del mismo event loop de cada `asyncio.run()`. Verificado localmente mandando 2 mensajes seguidos en el mismo proceso.

### 10. Filtro de rol (Fase 3, adelantada)

Primera corrida automática en GitHub Actions notificó ~100 ofertas de golpe (marketing, diseño, investigación en IA no relacionada a software, etc.) — sin filtro, Arbeitnow trae ofertas de todas las industrias, no solo software. El usuario decidió pasar de "MVP mínimo" a "pulir para que traiga justo lo que busca", así que se adelantó el filtro de rol de la Fase 3.

Se probó con datos reales: `tags` y `job_types` de Arbeitnow son inconsistentes (a veces vacíos, a veces con la categoría, a veces sin relación) — no sirven como filtro confiable por sí solos. Se implementó `src/processing/filters.py` con `is_relevant_role(title)`: combina keywords de dominio (software, developer, engineer, backend, frontend, devops, etc.) + nivel de entrada (intern, werkstudent, graduate, junior, trainee...) excluyendo senior/lead/staff/principal/manager. Sobre 250 ofertas reales, filtra a 4 genuinamente relevantes.

`main.py` ahora filtra **antes** de guardar en Mongo (no solo antes de notificar) — así la colección `jobs` no se llena de las ~98% de ofertas irrelevantes, importante en el tier gratis de Atlas (límite de 512MB).

Se limpiaron los 400 documentos irrelevantes que había sembrado la corrida anterior (sin filtro), dejando solo los 10 que sí son relevantes. Corrida real post-limpieza: 250 revisadas, 4 relevantes, 0 nuevas (ya estaban guardadas) — sin errores.

**Pendiente (no bloqueante):** filtro geográfico por región prioritaria (Austria, Suiza, Nórdicos). Arbeitnow solo da la ciudad, no el país, así que necesita un mapeo ciudad→país/región aparte — por ahora todas las regiones se dejan pasar (el plan ya definía "resto de Europa como secundario", no excluido).

**También pendiente:** revisar y borrar el sample dataset que Atlas cargó en el cluster (~140MB) a pesar de haberlo desmarcado — libera espacio del límite gratis de 512MB.

**Confirmado en producción:** corrida manual del workflow en GitHub Actions con el filtro ya activo → ✅ Success, 0 notificaciones (correcto, coincide con la prueba local — no había ofertas relevantes nuevas). El cron de cada 6h queda corriendo solo desde acá.

**InternScout está en producción:** fetch → filtro (software + entry-level) → dedupe (Mongo) → notificación (Telegram), automatizado cada 6h vía GitHub Actions, sin intervención manual.

### 11. Nuevo objetivo: prácticas en el extranjero (2026-10-06)

Tras ~3 semanas en producción, el proyecto pasa de "avisarme de ofertas" a **conseguir prácticas de software engineering en Austria, Suiza, Noruega, Suecia, Finlandia, Dinamarca y Alemania**: pagas (lo suficiente para vivir allá), de preferencia abiertas a extranjeros (visa/relocation), con más fuentes y mensajes más completos. LinkedIn/Indeed quedan fuera (anti-scraping y ToS).

Plan en 7 pasos: (1) pipeline multi-fuente, (2) filtro por país + rol multi-idioma, (3) fuentes nuevas, (4) etiquetado de salario/visa/prácticas no pagadas, (5) mensaje de Telegram completo con traducción al inglés (DeepL), (6) fuentes que requieren scraping (Noruega, Finlandia, Dinamarca, Karriere.at, jobs.ch) tras revisar sus términos, (7) pulido (`run_logs`, tests, actualizar Actions, limpiar sample dataset de Atlas).

Verificado con llamadas reales antes de planear: la API abierta de Suecia (`jobsearch.api.jobtechdev.se`) funciona sin key y trae país y duración, pero casi nunca el monto del salario; las APIs públicas de Lever y Greenhouse sirven las ofertas de empresas. Aún no hay fuente limpia verificada para Noruega, Finlandia y Dinamarca.

Antes de esto, el mensaje de Telegram se mejoró: ahora usa formato HTML (título en negrita, empresa y ubicación, fragmento de la descripción, enlace "Ver oferta" y fuente), escapando el texto con `html.escape`.

### 12. Paso 1: pipeline multi-fuente

- `src/collectors/base.py`: dataclass `RawPosting` (formato común de oferta) y clase abstracta `Collector` (`name` + `fetch() -> list[RawPosting]`). Se crea ahora porque ya se justifica: viene la segunda fuente.
- `src/collectors/arbeitnow.py`: pasa de función a `ArbeitnowCollector`, que devuelve `RawPosting`.
- `src/processing/normalizer.py`: `normalize(posting)` único para todas las fuentes (antes `normalize_arbeitnow_job`). El `job_hash` se calcula igual (título + empresa + URL), así que no hay duplicados. Se agregó el campo `country` al documento.
- `src/main.py`: recorre una lista `COLLECTORS`. Si el `fetch()` de una fuente falla, imprime el error, sigue con las demás y al final termina con error (para que GitHub Actions lo marque en rojo). Los errores de Mongo o Telegram siguen abortando la corrida.

Pruebas: el collector devuelve `RawPosting`; el hash coincide con los documentos ya guardados en Mongo (sin riesgo de renotificar ofertas viejas); una fuente simulada que falla no impide que Arbeitnow se procese y la corrida termina con `SystemExit`; corrida real: 325 ofertas revisadas, 6 relevantes, 4 notificadas.

Error mío durante las pruebas: la prueba de la fuente rota usó `seed=True` y sembró en silencio 4 ofertas relevantes aún no vistas (quedaron marcadas como notificadas sin avisar). Se identificaron por su `scraped_at` (solo esas 4 eran de los últimos 15 min), se borraron y la corrida real las notificó. Lección: una prueba que escribe en la base real no debe usar `--seed` sin comprobar antes si hay ofertas nuevas.

### 13. Paso 2: filtro por país y rol multi-idioma

**País.** `src/processing/geo.py` define, por cada uno de los 7 países, su nombre en varios idiomas, ciudades principales y regiones (Bundesländer, cantones, etc.). `detect_country(location)` normaliza el texto (sin tildes ni diéresis, vía `src/processing/text.py`) y busca coincidencias por palabra completa. El país lo fija el collector: Arbeitnow lo infiere de la ubicación; las fuentes propias de un país (como Suecia) lo pondrán directo. `main.py` descarta lo que no esté en `TARGET_COUNTRIES`. `PRIORITY_COUNTRIES` (todos menos Alemania) queda listo para el marcador de prioridad del paso 5.

**Rol.** `src/processing/filters.py` pasa de `is_relevant_role` a `classify_role(title)`, que devuelve `internship`, `graduate` o `entry_level` (o `None`) y se guarda como `role_type` en Mongo. Cambios de fondo:
- El inglés se compara por palabra completa y las demás lenguas por raíz (para palabras compuestas como `Softwareentwickler` o `praktikplats`). Esto corrige un defecto: antes "Internal Tools Developer" pasaba como práctica porque "internal" contiene "intern".
- Vocabulario en alemán, sueco, noruego, finlandés, danés, y términos suizos en francés/italiano.
- "engineer" sigue contando como señal de dominio (para no perder títulos como "Computational Geometry Engineer"), pero se excluyen disciplinas no software (mecánica, eléctrica, civil, química...), ventas/GTM, cargos senior/lead/manager y formaciones profesionales (Ausbildung, Fachinformatiker, duales Studium).
- Se quitó "apprentice" de los niveles de entrada: un aprendizaje (Lehre) no es una práctica universitaria.

**Calibración con datos reales** (325 ofertas de Arbeitnow): 150 caen en países objetivo (89 Alemania, 59 Suiza, 1 Austria); las ubicaciones sin reconocer eran casi todas Reino Unido, Francia, "Remote" o vacías (correctamente fuera). Tras el filtro de rol quedaron 3, de las cuales 2 eran falsos positivos (una formación de Fachinformatiker presentada como "Traumpraktikum" y un "Junior GTM Engineer" de ventas); se excluyeron y se agregaron como casos de test.

**Tests:** `tests/test_filters.py` y `tests/test_geo.py`, 54 casos (parte del paso 7 adelantada, porque el filtro ya es lo bastante complejo para necesitarlos).

**Conclusión:** con Arbeitnow solo, una página completa deja ~1 oferta relevante. El cuello de botella ahora son las fuentes, no los filtros. Corrida real: 150 en países objetivo, 1 relevante, 0 nuevas (ya guardada).

Siguiente: paso 3 (fuentes nuevas: Suecia, Adzuna, empresas vía Lever/Greenhouse).
