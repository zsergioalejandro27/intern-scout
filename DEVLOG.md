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

**Fase 0 completa.** Siguiente: implementar el collector de Arbeitnow (Fase 1 — MVP end-to-end).
