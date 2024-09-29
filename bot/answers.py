# /start
HOW_TO_USAGE = """
    Bienvenido! Este bot responde a la pregunta quién juega hoy?

    Los comandos con que me puedes llamar son:

    /todo
        Entrega todos los eventos disponibles
    /hoy
        Entrega los eventos del día (a la hora de Chile)
    /fecha <fecha>
        Entrega los eventos para la fecha dada, debe estar en formato YYYY-MM-DD
    /cuando <palabra>
        Entrega los eventos que contienen la palabra en el nombre del evento, canal o liga.
    /set_alias <tu equipo> <tu alias en una sola palabra>
        Agrega un alias para tu equipo favorito, para que puedas buscarlo más fácilmente.
    /version
        Entrega la versión del bot.

    Si eres ñoño como yo, te encantará saber cuales son las tecnologías usadas:
    - Python
    - FastAPI
    - GraphQL
    - ormar (SQLAlchemy)
    - Neon Tech (PostgreSQL)
    - pyTelegramBotAPI
    - Cloud Run
    """.strip()

# /fecha
DATE_WITHOUT_ARGS = """
    Debes enviar /fecha <fecha> en formato YYYY-MM-DD
""".strip()

DATE_WITH_NO_COINCIDENCES = """
    No hay eventos agendados aún para {} unu. Prueba con otra fecha
""".strip()

# /cuando
WHEN_WITHOUT_ARGS = """
    Debes enviar /cuando <una palabra>
""".strip()

WHEN_WITH_NO_COINCIDENCES = """
    No se encontraron eventos que contengan {} unu.
    Prueba escribiéndolo de otra forma.
""".strip()

# /todo
ALL_WITH_NO_COINCIDENCES = """
    No hay eventos disponibles, prueba más tarde {}.
""".strip()

# /version

VERSION = """
    3.17.1
""".strip()

# /set_alias

ALIAS_ADDED_SUCCESSFULLY = """
    Alias agregado correctamente!
""".strip()

ALIAS_WITHOUT_ARGS = """
    Debes enviar /set_alias <tu equipo> <tu alias en una sola palabra>
""".strip()

INVALID_COMMAND = """
    No entiendo el comando que me enviaste, prueba con /help para ver los comandos disponibles.
""".strip()

WAKING_UP = "Estaba despertando 🥱. Voy corriendo a procesarlo 🏃‍♂️‍➡️".strip()

SOMETHING_HAPPENED = "Algo salió mal, intenta más tarde 🥺".strip()

GENERATING_IMAGE = "Generando imagen... 📸".strip()

SENDING_IMAGE = "Enviando imagen... 🧳".strip()
