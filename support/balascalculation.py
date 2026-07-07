from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QColor

BalaNeededValues = {
    "Shadbala": {"Sun": 390, "Moon": 360, "Mars": 300, "Mercury": 420, "Jupiter": 390, "Venus": 330, "Saturn": 300},
    "Sthanabala": {"Sun": 165, "Moon": 133, "Mars": 96, "Mercury": 165, "Jupiter": 165, "Venus": 133, "Saturn": 96},
    "Digbala": {"Sun": 35, "Moon": 50, "Mars": 30, "Mercury": 35, "Jupiter": 35, "Venus": 50, "Saturn": 30},
    "Kaalabala": {"Sun": 80, "Moon": 70, "Mars": 60, "Mercury": 80, "Jupiter": 80, "Venus": 70, "Saturn": 60},
    "Cheshtabala": {"Sun": 112, "Moon": 100, "Mars": 67, "Mercury": 112, "Jupiter": 112, "Venus": 100, "Saturn": 67},
    "Ayanabala": {"Sun": 30, "Moon": 40, "Mars": 20, "Mercury": 30, "Jupiter": 30, "Venus": 40, "Saturn": 20}                    
}

def update_shadbala_progress_bar(progressbar, planet_name, shadbala_virupas):
    min_balas = {
        "Sun": 390,
        "Moon": 340,
        "Mars": 300,
        "Mercury": 360,
        "Jupiter": 390,
        "Venus": 330,
        "Saturn": 300,
        "Rahu": 1,
        "Ketu": 1,
        "Ascendant": 1
    }

    if planet_name not in min_balas:
        raise ValueError("Invalid planet name")

    min_value = min_balas[planet_name]

    # Map the minimum value to 50% of the progress bar
    if shadbala_virupas <= min_value:
        progress_value = (shadbala_virupas / min_value) * 50
        color = QColor(255, 0, 0)  # Red
    else:
        progress_value = 50 + ((shadbala_virupas - min_value) / (750 - min_value) * 50)
        color = QColor(0, 255, 0)  # Green

    progressbar.setValue(int(progress_value))
    progressbar.setStyleSheet(
        "QProgressBar::chunk { background-color: %s; }" % color.name()
    )

    progressbar.setFormat("%d%%" % progress_value)
    return min_value
