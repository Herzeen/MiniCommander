import sys
import os
import shutil
import json

# Importy PyQt5 – elementy GUI
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QTreeView, QLabel, QFileSystemModel,
    QDialog, QListWidget, QInputDialog, QMessageBox,
    QPushButton, QShortcut
)
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont, QKeySequence

# Plik konfiguracyjny z regułami sortowania
CONFIG_FILE = "config.json"


# =========================================================
# OKNO EDYCJI REGUŁ SORTOWANIA
# =========================================================
class ConfigEditor(QDialog):
    def __init__(self, rules):
        super().__init__()

        # Ustawienie tytułu okna
        self.setWindowTitle("Edytuj reguły")

        # Aktualne reguły przekazane z głównej aplikacji
        self.rules = rules

        # Layout pionowy
        layout = QVBoxLayout()

        # Lista wyświetlająca reguły
        self.list_widget = QListWidget()
        self.load_rules()

        # Przyciski operacji
        btn_add = QPushButton("Dodaj")
        btn_edit = QPushButton("Edytuj")
        btn_delete = QPushButton("Usuń")
        btn_save = QPushButton("Zapisz")

        # Podpięcie funkcji do przycisków
        btn_add.clicked.connect(self.add_rule)
        btn_edit.clicked.connect(self.edit_rule)
        btn_delete.clicked.connect(self.delete_rule)
        btn_save.clicked.connect(self.save_rules)

        # Dodanie elementów do layoutu
        layout.addWidget(self.list_widget)
        layout.addWidget(btn_add)
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    # Wczytanie reguł do listy
    def load_rules(self):
        self.list_widget.clear()
        for folder, exts in self.rules.items():
            self.list_widget.addItem(f"{folder}: {', '.join(exts)}")

    # Dodanie nowej reguły
    def add_rule(self):
        folder, ok = QInputDialog.getText(self, "Folder", "Nazwa folderu:")
        if ok and folder:
            exts, ok = QInputDialog.getText(self, "Rozszerzenia", "(.jpg,.png):")
            if ok:
                self.rules[folder] = [e.strip().lower() for e in exts.split(",") if e.strip()]
                self.load_rules()

    # Edycja istniejącej reguły
    def edit_rule(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        folder = item.text().split(":")[0]
        exts = ",".join(self.rules[folder])

        new_exts, ok = QInputDialog.getText(self, "Edytuj", "Rozszerzenia:", text=exts)
        if ok:
            self.rules[folder] = [e.strip().lower() for e in new_exts.split(",") if e.strip()]
            self.load_rules()

    # Usunięcie reguły
    def delete_rule(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        folder = item.text().split(":")[0]
        self.rules.pop(folder, None)
        self.load_rules()

    # Zapis reguł do pliku JSON
    def save_rules(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.rules, f, indent=4)
            QMessageBox.information(self, "OK", "Zapisano!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))


# =========================================================
# GŁÓWNA APLIKACJA
# =========================================================
class FileManager(QWidget):
    def __init__(self):
        super().__init__()

        # Usunięcie standardowego paska okna
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Rozmiar okna i font
        self.setGeometry(100, 100, 1100, 600)
        self.setFont(QFont("Consolas", 10))

        # Wczytanie reguł
        self.rules = self.load_config()

        # Aktywny panel (lewy/prawy)
        self.active_panel = "left"

        # Layouty
        main_layout = QVBoxLayout()
        panels_layout = QHBoxLayout()

        # Model plików (system plików)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # LEWY PANEL
        self.left_view = QTreeView()
        self.left_view.setModel(self.model)
        self.left_view.setRootIndex(self.model.index(os.getcwd()))

        # PRAWY PANEL
        self.right_view = QTreeView()
        self.right_view.setModel(self.model)
        self.right_view.setRootIndex(self.model.index(os.getcwd()))

        panels_layout.addWidget(self.left_view)
        panels_layout.addWidget(self.right_view)

        # Pasek informacji
        self.info_label = QLabel("Gotowe")

        # Pasek skrótów klawiszowych
        self.footer = QLabel(
            " TAB panel | ENTER otwórz | BACK cofaj | F5 kopiuj | F6 przenieś | F7 sortuj | F8 reguły | F10 wyjście "
        )

        # Składanie layoutu
        main_layout.addLayout(panels_layout)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.footer)

        self.setLayout(main_layout)

        # Skrót TAB (zmiana panelu)
        self.tab_shortcut = QShortcut(QKeySequence("Tab"), self)
        self.tab_shortcut.activated.connect(self.switch_panel)

        self.update_active_panel_style()

    # =========================================================
    # PANEL
    # =========================================================
    def switch_panel(self):
        if self.active_panel == "left":
            self.active_panel = "right"
            self.right_view.setFocus()
        else:
            self.active_panel = "left"
            self.left_view.setFocus()

        self.update_active_panel_style()

    # Wizualne zaznaczenie aktywnego panelu
    def update_active_panel_style(self):
        if self.active_panel == "left":
            self.left_view.setStyleSheet("border: 2px solid yellow;")
            self.right_view.setStyleSheet("border: 1px solid gray;")
        else:
            self.right_view.setStyleSheet("border: 2px solid yellow;")
            self.left_view.setStyleSheet("border: 1px solid gray;")

    # Pobranie aktywnego panelu
    def get_active_view(self):
        return self.left_view if self.active_panel == "left" else self.right_view

    # Pobranie drugiego panelu
    def get_other_view(self):
        return self.right_view if self.active_panel == "left" else self.left_view

    # =========================================================
    # NAWIGACJA
    # =========================================================
    def open_dir(self):
        view = self.get_active_view()
        index = view.currentIndex()

        if self.model.isDir(index):
            view.setRootIndex(index)

    def go_up(self):
        view = self.get_active_view()
        current = self.model.filePath(view.rootIndex())
        parent = os.path.dirname(current)
        view.setRootIndex(self.model.index(parent))

    # =========================================================
    # FUNKCJE POMOCNICZE
    # =========================================================
    def get_unique_name(self, path):
        base, ext = os.path.splitext(path)
        i = 1
        while os.path.exists(path):
            path = f"{base}({i}){ext}"
            i += 1
        return path

    # =========================================================
    # OPERACJE NA PLIKACH
    # =========================================================
    def copy_file(self):
        try:
            src = self.get_active_view()
            dst = self.get_other_view()

            src_path = self.model.filePath(src.currentIndex())
            target_dir = self.model.filePath(dst.rootIndex())

            name = os.path.basename(src_path)
            target_path = self.get_unique_name(os.path.join(target_dir, name))

            if os.path.isdir(src_path):
                shutil.copytree(src_path, target_path)
            else:
                shutil.copy2(src_path, target_path)

            self.info_label.setText("Skopiowano")

        except Exception as e:
            self.info_label.setText(f"Błąd: {e}")

    def move_file(self):
        try:
            src = self.get_active_view()
            dst = self.get_other_view()

            src_path = self.model.filePath(src.currentIndex())
            target_dir = self.model.filePath(dst.rootIndex())

            name = os.path.basename(src_path)
            target_path = self.get_unique_name(os.path.join(target_dir, name))

            shutil.move(src_path, target_path)
            self.info_label.setText("Przeniesiono")

        except Exception as e:
            self.info_label.setText(f"Błąd: {e}")

    # =========================================================
    # SORTOWANIE
    # =========================================================
    def sort_files(self):
        try:
            view = self.get_active_view()
            folder = self.model.filePath(view.rootIndex())

            for f in os.listdir(folder):
                path = os.path.join(folder, f)

                if os.path.isfile(path):
                    ext = os.path.splitext(f)[1].lower()
                    target = "Inne"

                    for k, v in self.rules.items():
                        if ext in v:
                            target = k
                            break

                    target_path = os.path.join(folder, target)
                    os.makedirs(target_path, exist_ok=True)

                    shutil.move(path, self.get_unique_name(os.path.join(target_path, f)))

            self.info_label.setText("Sortowanie OK")

        except Exception as e:
            self.info_label.setText(f"Błąd: {e}")

    # =========================================================
    # EDYTOR REGUŁ
    # =========================================================
    def open_config_editor(self):
        editor = ConfigEditor(self.rules)
        if editor.exec_():
            self.rules = self.load_config()

    # =========================================================
    # CONFIG
    # =========================================================
    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            default = {"Obrazy": [".jpg"], "Dokumenty": [".pdf"], "Inne": []}
            with open(CONFIG_FILE, "w") as f:
                json.dump(default, f, indent=4)
            return default

        with open(CONFIG_FILE) as f:
            return json.load(f)

    # =========================================================
    # OBSŁUGA KLAWIATURY
    # =========================================================
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.open_dir()
        elif event.key() == Qt.Key_Backspace:
            self.go_up()
        elif event.key() == Qt.Key_F5:
            self.copy_file()
        elif event.key() == Qt.Key_F6:
            self.move_file()
        elif event.key() == Qt.Key_F7:
            self.sort_files()
        elif event.key() == Qt.Key_F8:
            self.open_config_editor()
        elif event.key() == Qt.Key_F10:
            self.close()


# =========================================================
# START PROGRAMU
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Styl DOS
    app.setStyleSheet("""
        QWidget { background-color: #000080; color: #FFFF00; font-family: Consolas; }
        QTreeView { background-color: #000080; color: #FFFFFF; }
        QTreeView::item:selected { background-color: yellow; color: black; }
    """)

    window = FileManager()
    window.show()
    sys.exit(app.exec_())