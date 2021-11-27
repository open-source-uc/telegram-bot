# Bot Newbie Open Source UC

Estos 2 bots tienen como principal función hacer el inicio al grupo mucho más comodo y fluido, para que sepa que es lo que debe realizar cuando se une al grupo.

Se debe crear un .env con el TELEGRAM_API_TOKEN y TELEGRAM_API_TOKEN_2, ademas de que el bot 1 (main.py) debe ser puesto como administrador de grupo para poder leer cuando alguien ingresa al grupo.

## Instalacion

```bash
pip3 install poetry
poetry install

poetry shell

python -m osuc_companion
```

### Crear env

- Obtener 2 API key de telegram
- `$ cp .env.example .env`
- Remplazar valores para la API

## Antes de hacer commit

```bash
black osuc_companion
isort osuc_companion
```

## Matenimiento

### `conversation.py`

  En `osuc_companion/text/replies.json` se pueden encontrar los textos de respuesta utilizados.