from forecast.forecast_service import moving_average_forecast, max_percent_change

import sys
import pandas as pd

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


# Путь к файлу задаётся вручную
DATA_FILE = "samples/migration.csv"


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Анализ миграции населения")
        self.resize(1000, 700)

        self.df = pd.read_csv(DATA_FILE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Панель параметров
        controls = QHBoxLayout()

        controls.addWidget(QLabel("Окно средней:"))

        self.window_size = QSpinBox()
        self.window_size.setRange(2, 20)
        self.window_size.setValue(3)
        self.window_size.valueChanged.connect(self.update_plot)

        controls.addWidget(self.window_size)

        controls.addWidget(QLabel("Прогноз лет:"))

        self.forecast_years = QSpinBox()
        self.forecast_years.setRange(1, 20)
        self.forecast_years.setValue(5)
        self.forecast_years.valueChanged.connect(self.update_plot)

        controls.addWidget(self.forecast_years)

        controls.addWidget(QLabel(f"Максимальное изменение эмиграции: {round(max_percent_change(self.df["emmigration"])[1])}%"))

        controls.addStretch()

        layout.addLayout(controls)

        # График
        self.canvas = MplCanvas()
        layout.addWidget(self.canvas)

        self.update_plot()

    def update_plot(self):
        n = self.window_size.value()
        forecast = self.forecast_years.value()

        years = self.df["year"].tolist()
        immigration = self.df["immigration"].tolist()
        emigration = self.df["emmigration"].tolist()

        future_years = list(
            range(years[-1] + 1, years[-1] + forecast + 1)
        )

        immigration_forecast = moving_average_forecast(
            immigration,
            n,
            forecast
        )

        emigration_forecast = moving_average_forecast(
            emigration,
            n,
            forecast
        )

        ax = self.canvas.ax
        ax.clear()

        ax.plot(
            years,
            immigration,
            label="Иммиграция"
        )

        ax.plot(
            years,
            emigration,
            label="Эмиграция"
        )

        ax.plot(
            future_years,
            immigration_forecast[-forecast:],
            "--",
            label="Прогноз иммиграции"
        )

        ax.plot(
            future_years,
            emigration_forecast[-forecast:],
            "--",
            label="Прогноз эмиграции"
        )

        ax.set_title("Миграция населения")
        ax.set_xlabel("Год")
        ax.set_ylabel("Количество человек")
        ax.grid(True)
        ax.legend()

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
