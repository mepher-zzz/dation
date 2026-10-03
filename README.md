# Dation · Obras a la vista

Consulta ciudadana de fichas aprobadas sin cuenta, con fotografías, fechas y fuentes. La aplicación local permite preparar borradores manualmente o con Gemini, cargar evidencia, revisar y aprobar versiones con cuentas autorizadas. La gestión usa una paleta azul e índigo y una barra de área restringida. Conserva Python, FastAPI, Jinja, Pydantic y Pillow; el antiguo constructor de Gradio sigue disponible como biblioteca.

La demostración hospedada contiene únicamente dos casos ficticios y consulta ciudadana. El área de escritura funciona en la aplicación Python local. El alojamiento disponible no ejecuta Python; no se presenta el sitio estático como un sistema institucional en línea.

## Iniciar la aplicación completa

Desde esta carpeta, con Python 3.14 y `uv`:

```powershell
uv sync
uv run python tools/manage_accounts.py mi-administrador
uv run python main.py
```

El segundo comando pide una contraseña de al menos 12 caracteres sin mostrarla. Se ejecuta una vez por cuenta. No hay credenciales predeterminadas ni registro público.

Abre **http://127.0.0.1:7860/acceso**. «Entrar sin cuenta» conduce a `/obras` y permite consultar únicamente fichas aprobadas. Ingresa con una cuenta autorizada para abrir `/institucional`. También funciona `uv run ai-gemini-test`; `/estudio` conduce al área institucional. Detén el servidor con `Ctrl+C`. Si ya estaba ejecutándose, reinícialo para cargar los cambios.

Para análisis real, configura `GEMINI_API_KEY` en `.env` y deja `DEMO_MODE` desactivado. No hace falta una clave para trabajar manualmente, revisar o consultar fichas. Sin clave, la solicitud de análisis explica el problema y conserva la evidencia y el borrador. Se verificaron llamadas reales y el flujo completo con dos ilustraciones sintéticas el 2 de octubre de 2026; las pruebas automatizadas usan respuestas sintéticas y no envían fotografías reales.

## Preparar y aprobar una ficha

1. Administración crea cuentas desde «Gestión de fichas» y asigna consulta, autor, revisor o administrador. Puede cambiar permisos, desactivar cuentas y asignar responsables. Estos cambios se verifican en servidor.
2. Un autor o administrador elige «Nueva ficha» y selecciona «Con inteligencia artificial» o «De forma manual». Ambas opciones se pueden combinar; los textos manuales existentes se conservan durante el análisis.
3. Selecciona JPEG, PNG o WebP: de 1 a 30 fotografías, hasta 20 MB por archivo. El tablero muestra miniaturas antes de cargar. Selecciona una imagen para configurar fecha, sector, nota, fuente y permiso en un panel; también puedes hacerlo después de guardarla. La fecha vacía representa una fecha desconocida. Subir/Bajar permite ordenar la evidencia.
4. «Analizar fotografías y completar con IA» guarda los cambios y archivos pendientes, analiza cada foto y compara la serie. Una barra muestra las etapas completadas y los resultados preliminares. El resultado completo aparece en la misma página y se guarda como borrador. Gemini completa descripciones, sectores, tipo de obra, textos ciudadanos y datos legibles en carteles cuando los campos están vacíos. En análisis posteriores actualiza las propuestas anteriores que no hayas modificado. Las fechas desconocidas, permisos y datos documentales requieren confirmación humana. «Datos adicionales» conserva presupuesto, hitos y avisos; «Análisis original e historial interno» mantiene la respuesta y revisiones.
5. Guarda y envía a revisión. Durante la revisión no se edita el borrador. Revisor y administrador pueden devolverlo con observaciones o aprobarlo después de confirmar fuentes, narración, límites y permisos. Administración también puede devolver sus propios borradores para corregirlos.
6. La aprobación publica una nueva versión en `/obras/{id}`. El enlace se mantiene estable y la versión anterior continúa visible hasta aprobar la siguiente. Se impide aprobar la propia ficha o la versión que uno preparó.
7. Solo administración dispone de «Eliminar» en el listado y en el editor, para cualquier estado. Tras confirmar, se borran definitivamente ficha, versiones, historial de borradores, originales y derivados; queda un evento mínimo de auditoría. Para retirar una ficha conservando su contenido, usa «Archivar».

El año del explorador significa **año de captura de la evidencia**, no inicio de obra ni año de edición. Las alternativas dentro de un filtro se unen; distintos filtros se combinan. Las fichas distinguen fecha de evidencia, revisión, datos documentales y observaciones.

## Informes heredados y ejemplos

Los informes de `.reports/` se conservaron; no pasan automáticamente a consulta ciudadana. Para incorporar un informe antiguo a gestión, asignándolo como borrador privado:

```powershell
uv run python tools/import_report.py ID_EXISTENTE --owner NOMBRE_DE_AUTOR
```

El responsable debe existir y estar activo. La importación conserva la respuesta original y exige revisar permisos antes de publicar. Algunos registros antiguos solo conservan WebP sin originales: se pueden editar sus datos y narración, pero el análisis exige originales de todos los registros seleccionados.

Para agregar los dos ejemplos explícitos al entorno local:

```powershell
uv run python tools/seed_demo.py
```

Es una carga de fixtures ficticios para presentar la interfaz; no equivale a revisión humana real. La demostración individual no sugiere cambio o tendencia. `DEMO_MODE=true` activa respuestas deterministas de prueba, identificadas como demostración; no debe utilizarse para producir informes reales.

## Privacidad y almacenamiento

- La consulta `/obras`, sus fichas aprobadas y sus fotografías derivadas no requieren cuenta. Borradores, API de gestión, miniaturas internas, originales y administración requieren sesión y permisos. Las fichas archivadas y eliminadas dejan de estar disponibles a la ciudadanía.
- `.dation/workflow.sqlite3` almacena cuentas con scrypt, sesiones con tokens aleatorios y caducidad, borradores, revisiones, versiones aprobadas y auditoría. Los originales nuevos quedan en `.dation/originals/`; sus derivados WebP sin EXIF, en `.reports/`.
- Un autor trabaja sobre sus fichas. Revisor y administrador pueden consultar la evidencia para sus funciones; consulta solo ve versiones aprobadas. Cambiar permisos invalida las sesiones de esa cuenta.
- Compartir o enviar por WhatsApp copia el enlace de la ficha aprobada, que puede consultarse sin cuenta. No se añadieron analítica, seguimiento, invitaciones ni afiliación institucional.
- Respalda `.dation/` y `.reports/` juntos. Nunca publiques estas carpetas ni `.env`. Usa un único proceso de servidor: las cargas están serializadas por ficha y las versiones usan transacciones SQLite; no se validó escritura con múltiples procesos.

El servidor escucha en loopback. Para otro servidor privado Python, configura HTTPS, un proxy de confianza y `DATION_HOSTNAME`; `HOST=0.0.0.0` exige ese nombre. Antes de uso institucional real hacen falta evaluación operativa, política de conservación, identidad institucional y recuperación de cuentas. No hay integración oficial con la Contraloría.

## Demostración privada hospedada

`tools/export_demo.py` genera `dist/` desde las mismas vistas y una base temporal con datos exclusivamente ficticios. Exporta catálogo, dos fichas, búsqueda/filtros en navegador y derivados de ilustraciones; no exporta análisis originales, cuentas, borradores, registros reales ni el libro. `.openai/hosting.json` vincula el único sitio de Sites, con acceso del propietario. La publicación se realiza mediante el flujo de Sites y aprobación privada de la plataforma; copiar `dist` a un servidor sin autenticación no conserva esa privacidad.

## Validación y documentación

```powershell
uv run python -m unittest discover -s tests
uv run ruff check src tests tools main.py create_demo_report.py
uv run ruff format --check src tests tools main.py create_demo_report.py
uv run mypy main.py src create_demo_report.py
uv build --out-dir .qa/package
```

La revisión de navegador adicional requiere Playwright, Chrome y una copia local de axe-core 4.10.3 en `.qa/axe.min.js`. Se ejecuta con `python tools/check_browser.py` después de instalar Playwright en el entorno de revisión. Usa cuentas y datos temporales sintéticos, sin claves de IA.

- [Diseño, feedback, conservación de datos y Krug](docs/design-and-data.md).
- [Investigación, validación y prueba con personas pendiente](docs/research-and-tests.md).
- [Capturas, PDF de ejemplo y resultados del navegador](artifacts/README.md).

La validación automática no demuestra accesibilidad completa ni comprensión por personas usuarias. La prueba cualitativa y la comprobación con lector de pantalla siguen pendientes.

