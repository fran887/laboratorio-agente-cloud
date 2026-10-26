# Laboratorio 12 — Agente cloud

- **Repositorio:** https://github.com/fran887/laboratorio-agente-cloud
- **Agente:** GitHub Copilot coding agent (`app/copilot-swe-agent`)
- **Entorno remoto:** runner efímero de GitHub Actions (`Copilot cloud agent`)
- **Modalidad:** delegación asíncrona por asignación de issue; el agente publica rama + PR y nosotros revisamos.

## Artefactos

| # | Artefacto | Enlace |
|---|---|---|
| 1 | Issue original (categorías y filtrado) | https://github.com/fran887/laboratorio-agente-cloud/issues/1 |
| 2 | PR generado por el agente (categorías) | https://github.com/fran887/laboratorio-agente-cloud/pull/2 |
| 3 | Issue del reto final (eliminar por ID) | https://github.com/fran887/laboratorio-agente-cloud/issues/3 |
| 4 | PR generado por el agente (eliminar por ID) | https://github.com/fran887/laboratorio-agente-cloud/pull/4 |

## Evidencia en `evidencias/`

| Archivo | Contenido |
|---|---|
| `01_linea_base.txt` | `python3 app.py` y `unittest` antes de delegar (2 pruebas OK) |
| `02_bloqueo_copilot.txt` | `gh agent-task create` → 403 en `api.individual.githubcopilot.com` (cuenta sin Copilot) |
| `03_bloqueo_codex.txt` | Codex Cloud sin environments y sin acceso al repo |
| `04_validacion_local_main.txt` | Suite local tras integrar el PR #2 (5 pruebas) |
| `05_diff_pr2.txt` | Diff completo del PR #2 |
| `06_pr2_estado_checks.txt` | Estado del PR #2 y runs de Actions |
| `07_revision_iteracion_pr2.txt` | Revisión humana + respuesta del agente (iteración) |
| `08_issue1.png`, `09_pr2_conversacion.png`, `10_pr2_files.png` | Capturas del issue y del PR #2 |
| `11_validacion_local_pr4.txt` | Suite local y `app.py` tras integrar el PR #4 (8 pruebas) |
| `12_diff_pr4.txt` | Diff completo del PR #4 |
| `13_revision_iteracion_pr4.txt` | Revisión humana + respuesta del agente (iteración) |
| `14_runs_pr4.txt` | Runs de Actions y estado final del PR #4 |
| `15_issue3.png`, `16_pr4_conversacion.png`, `17_pr4_files.png`, `18_ci_main.png` | Capturas del reto final y del CI en `main` |

## Ciclo de trabajo observado

1. Issue con objetivo, alcance, restricciones, criterios de aceptación y comando de validación.
2. Asignación a `copilot-swe-agent`; el agente trabaja en un runner remoto, crea rama `copilot/...`, commits y PR en borrador.
3. Revisión del diff archivo por archivo y ejecución local de la suite.
4. Comentario de revisión `@copilot` con un caso no cubierto; el agente actualiza **el mismo PR** (nuevo commit).
5. Validación local, marcado como *ready for review* y merge.

### Hallazgos reales de la revisión

- **PR #2:** el agente versionó `__pycache__/*.pyc`. Se pidió eliminarlos y agregar `.gitignore`; la segunda iteración lo corrigió y añadió la prueba de categoría inexistente.
- **PR #4:** `agregar_tarea` calculaba `id = len(tareas) + 1`; tras eliminar una tarea, el siguiente `id` se duplicaba (`[1, 3, 3]`). Se pidió corregirlo con `max(ids) + 1` y una prueba de regresión; la segunda iteración lo corrigió (`[1, 3, 4]`).

### Sobre los checks del PR

Los workflows disparados por PRs del coding agent quedan en `action_required` (GitHub exige aprobación humana de un mantenedor para ejecutar Actions en PRs del agente). Por eso:

- la ejecución del agente sí quedó registrada (`Copilot cloud agent`, éxito);
- la suite se validó **localmente** sobre cada rama y sobre `main`;
- el push de merge a `main` ejecutó `tests` en verde (9 s, 8 pruebas).

## Preguntas de reflexión

1. **CLI agent vs agente cloud.** El CLI corre como proceso local, de forma interactiva y con los permisos/archivos de mi máquina; el agente cloud corre en un entorno remoto efímero, de forma asíncrona, y devuelve una rama/PR aunque mi equipo esté apagado. El CLI no deja una frontera de revisión por sí solo; el cloud sí (rama + PR + checks + trazabilidad).
2. **Qué siguió sin mí.** Aprovisionamiento del entorno, instalación de Python, edición de archivos, ejecución de `unittest`, commits, push de la rama y apertura del PR. Yo solo consulté estado y revisé; ningún proceso local ejecutaba el trabajo.
3. **Por qué el PR es buena frontera.** Aísla el cambio en una rama, permite diff por archivo, ejecuta checks sobre el resultado, habilita comentarios y deja la decisión de merge en un humano. El agente no puede escribir en `main` sin aprobación.
4. **Riesgo de auto-merge.** Integrar sin revisión convierte errores en deuda inmediata: en este laboratorio se habrían colado `.pyc` y una colisión de `id` que las pruebas del agente no cubrían. Además, un check verde solo prueba los casos ejecutados, no la corrección total; también hay riesgo de cambios de alcance, dependencias no deseadas y prompt injection desde el repositorio.
5. **Issue delegable.** Objetivo, alcance (archivos), restricciones (sin dependencias, compatibilidad), criterios de aceptación verificables, comando de validación y definición de "terminado"; sin ambigüedades que obliguen a preguntar.
6. **Cuándo usar cloud vs interactivo.** Cloud para tareas acotadas, mecánicas y cubiertas por pruebas (tests, refactors con especificación, issues pequeños). Interactivo para diseño ambiguo, arquitectura, depuración con retroalimentación rápida y decisiones sensibles de seguridad.

## Reproducción local

```bash
git clone https://github.com/fran887/laboratorio-agente-cloud.git
cd laboratorio-agente-cloud
python3 app.py
python3 -m unittest discover -s tests
```
