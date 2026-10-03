"""Create a clearly labelled local demo report for visual review only."""

from __future__ import annotations

import argparse
import tempfile
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw

from ai_gemini_test.report_store import ProjectMetadata, save_report


def draw_demo_scene(path: Path, frame: int) -> None:
    """Draw an illustrative scene; these are never presented as real photos."""

    image = Image.new("RGB", (1200, 720), "#d5ebed")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1200, 380), fill="#cde8eb")
    draw.ellipse((930, 70, 1030, 170), fill="#fff4d4")
    draw.polygon(
        [
            (0, 400),
            (280, 315),
            (570, 390),
            (840, 290),
            (1200, 390),
            (1200, 720),
            (0, 720),
        ],
        fill="#80a78e",
    )
    draw.rectangle((0, 480, 1200, 720), fill="#aa9c83")
    draw.polygon([(90, 720), (420, 465), (780, 465), (1110, 720)], fill="#cab99d")

    stage = frame / 19
    if stage > 0.12:
        for x in (260, 540, 820):
            draw.rectangle((x, 490, x + 45, 630), fill="#aaa79a")
            draw.rectangle((x - 15, 620, x + 60, 645), fill="#8e8a80")
    if stage > 0.34:
        draw.polygon([(170, 472), (940, 472), (970, 505), (145, 505)], fill="#d6d3ca")
        draw.line([(170, 472), (940, 472)], fill="#717f83", width=6)
    if stage > 0.56:
        for x in range(185, 940, 115):
            draw.rectangle((x, 433, x + 7, 473), fill="#717d7d")
        draw.line([(185, 440), (940, 440)], fill="#717d7d", width=7)
    if stage > 0.74:
        draw.polygon([(425, 485), (775, 485), (1110, 720), (90, 720)], fill="#525f66")
        draw.line([(599, 510), (599, 700)], fill="#f5e8c8", width=8)
    if stage > 0.83:
        for x, y in ((240, 585), (850, 600), (1000, 685)):
            draw.rectangle((x, y - 36, x + 12, y), fill="#d36f35")
            draw.ellipse((x - 5, y - 45, x + 17, y - 26), fill="#ef9a50")

    if stage < 0.6:
        draw.rectangle((85, 470, 210, 500), fill="#df9a37")
        draw.rectangle((115, 435, 164, 475), fill="#bd7c2d")
        draw.ellipse((102, 492, 132, 522), fill="#283f45")
        draw.ellipse((177, 492, 207, 522), fill="#283f45")
        draw.line([(193, 441), (270, 384), (292, 388)], fill="#b97c32", width=15)

    image.save(path, quality=85)
    image.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(".reports"))
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="obra-demo-") as temporary:
        paths: list[str] = []
        for index in range(20):
            path = Path(temporary) / f"ilustracion-{index + 1:02d}.jpg"
            draw_demo_scene(path, index)
            paths.append(str(path))

        analysis = {
            "executive_summary": (
                "En esta demostración, la serie ilustra el paso de cimentación "
                "a una vía pavimentada con canalización temporal."
            ),
            "initial_state": (
                "Terreno intervenido, cimentación visible y maquinaria ilustrada."
            ),
            "final_state": (
                "Vía pavimentada ilustrada con barandas y canalización temporal."
            ),
            "progress_trend": "consistent_progress",
            "progress_evidence": [
                "Imágenes 1–8: aparecen apoyos y un tablero ilustrado.",
                "Imágenes 9–15: se incorporan barandas.",
                "Imágenes 16–20: aparece la superficie pavimentada.",
            ],
            "phase_transitions": [
                "Imágenes 1–8: cimentación a estructura aparente.",
                "Imágenes 16–20: pavimentación ilustrada.",
            ],
            "timeline_observations": [
                f"Imagen {number}: {('cimentación' if number < 8 else 'estructura' if number < 16 else 'pavimentación')} ilustrada."
                for number in range(1, 21)
            ],
            "safety_consistency": "partially_observed",
            "positive_safety_practices": [
                "Imágenes 17–20: elementos ilustrados de canalización temporal."
            ],
            "recurring_safety_concerns": [
                "La escena ficticia no permite verificar protección de todo el sitio."
            ],
            "resource_changes": [
                "Maquinaria: excavadora ilustrada al inicio y no visible al final.",
                "Materiales: elementos de baranda y pavimento ilustrados al final.",
                "Personal: no se representan personas; no puede estimarse el cambio.",
            ],
            "resource_comparison": {
                "personnel": None,
                "machinery": {
                    "initial_state": "Excavadora ilustrada en la primera imagen.",
                    "final_state": "No aparece en la última imagen.",
                    "visible_change": "La excavadora deja de aparecer en el encuadre.",
                    "related_images": [1, 20],
                },
                "materials": {
                    "initial_state": "Se ilustran apoyos de concreto.",
                    "final_state": "Se ilustran barandas y superficie pavimentada.",
                    "visible_change": "Aparecen nuevos elementos en la escena ficticia.",
                    "related_images": [1, 20],
                },
            },
            "conclusions": [
                "La secuencia ilustrada presenta cambios compatibles con progreso."
            ],
            "recommended_checks": [
                "En una obra real, contrastar avance con bitácora y cronograma oficial."
            ],
            "limitations": [
                "Estas imágenes son ilustraciones de prueba, no fotografías de una obra.",
                "Sin cronograma, presupuesto ni fuente oficial vinculados.",
                "No puede evaluarse seguridad real con ilustraciones.",
            ],
            "confidence": 0.85,
        }
        metadata = ProjectMetadata(
            name="Demostración de interfaz · paso vial ficticio",
            demo=True,
            location="Ubicación ficticia; no corresponde a Limoncito",
            purpose="Mostrar cómo se presenta el seguimiento público de una obra.",
            capture_dates=[
                date(2026, 5, 10) + timedelta(days=7 * i) for i in range(20)
            ],
        )
        report = save_report(analysis, paths, metadata, args.root)
        print(f"/obras/{report.id}")


if __name__ == "__main__":
    main()
