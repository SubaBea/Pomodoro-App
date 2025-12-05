import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import json
import csv
from datetime import datetime
from pathlib import Path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

MUNKA_PERCEK = 1
MUNKA_MASODPERC = 0

SZUNET_PERCEK = 0
SZUNET_MASODPERC = 5

HOSSZU_SZUNET_PERCEK = 0
HOSSZU_SZUNET_MASODPERC = 5

TANTARGYAK = [
    "Matematika", "Magyar nyelv", "Irodalom", "Történelem",
    "Angol", "Biológia", "Földrajz", "Fizika", "Kémia"
]

LOCAL_STAT_FILE = "pomodoro_session_log.json"

BASE_DIR = Path(__file__).resolve().parent
CSV_EXPORT_FILE = BASE_DIR / "Pomodoro_teljes_naplo.csv"

TODAY_DATE = datetime.now().strftime("%Y-%m-%d")

class PomodoroApp(toga.App):

    def frissit_ido_label(self):
        self.ido_label.text = f"{self.minutes:02d}:{self.seconds:02d}"

    def frissit_szin(self):

        if self.is_break:
            if self.pomodoro_cycle % 4 == 0 and self.pomodoro_cycle != 0:
                self.ido_label.style.color = "blue"
                self.mod_label.text = "Hosszú szünet"
                self.mod_label.style.color = "blue"
            else:
                self.ido_label.style.color = "green"
                self.mod_label.text = "Szünet"
                self.mod_label.style.color = "green"
        else:
            self.ido_label.style.color = "black"
            self.mod_label.text = "Tanulási idő"
            self.mod_label.style.color = "black"

    def beallit_munka_idot(self):

        self.minutes = MUNKA_PERCEK
        self.seconds = MUNKA_MASODPERC

    def beallit_szunet_idot(self):

        if self.pomodoro_cycle % 4 == 0 and self.pomodoro_cycle != 0:
            self.minutes = HOSSZU_SZUNET_PERCEK
            self.seconds = HOSSZU_SZUNET_MASODPERC
            print("Hosszú szünet beállítva.")
        else:
            self.minutes = SZUNET_PERCEK
            self.seconds = SZUNET_MASODPERC
            print("Rövid szünet beállítva.")

    def startup(self):
        self.is_running = False
        self.is_break = False
        self.pomodoro_cycle = 0

        self.session_log = []

        self.daily_summary = {}

        self.statisztika_labels = {}

        self.minutes = MUNKA_PERCEK
        self.seconds = MUNKA_MASODPERC

        main_box = toga.Box(
            style=Pack(direction=ROW, alignment="center", padding=20)
        )

        bal_panel = toga.Box(
            style=Pack(direction=COLUMN, padding_right=40, align_items="center")
        )
        jobb_panel = toga.Box(
            style=Pack(direction=COLUMN, padding_left=60, align_items="center")
        )

        tantargy_box = toga.Box(
            style=Pack(direction=ROW, padding=5, width=320)
        )

        tantargy_label = toga.Label(
            "Tantárgy:",
            style=Pack(padding_right=10, font_size=12)
        )

        self.tantargy_valaszto = toga.Selection(
            items=TANTARGYAK,
            style=Pack(width=220, font_size=12)
        )
        self.tantargy_valaszto.value = TANTARGYAK[0]

        tantargy_box.add(tantargy_label)
        tantargy_box.add(self.tantargy_valaszto)

        self.mod_label = toga.Label(
            "Tanulási idő",
            style=Pack(padding_top=25, font_size=20, font_weight="bold")
        )

        self.ido_label = toga.Label(
            "",
            style=Pack(
                padding_top=15,
                padding_bottom=25,
                font_size=44,
                color="black"
            )
        )

        self.frissit_ido_label()
        self.frissit_szin()

        gomb_box = toga.Box(
            style=Pack(direction=ROW, padding=10, width=260, justify_content="center")
        )

        self.start_stop_button = toga.Button(
            "Start",
            on_press=self.on_start_stop_gomb,
            style=Pack(padding_right=10, width=110, font_size=12)
        )

        reset_button = toga.Button(
            "Törlés",
            on_press=self.on_reset_gomb,
            style=Pack(width=110, font_size=12)
        )

        export_button = toga.Button(
            "Statisztika mentése",
            on_press=self.on_statisztika_mentese,
            style=Pack(margin_top=15, height=40, width=230, font_size=12)
        )

        gomb_box.add(self.start_stop_button)
        gomb_box.add(reset_button)

        bal_panel.add(tantargy_box)
        bal_panel.add(self.mod_label)
        bal_panel.add(self.ido_label)
        bal_panel.add(gomb_box)

        separator = toga.Box(
            style=Pack(
                height=1,
                width=320,
                background_color="#cccccc",
                padding_top=15,
                padding_bottom=15,
            )
        )
        bal_panel.add(separator)
        bal_panel.add(export_button)

        stat_cim = toga.Label(
            f"Tanulási idő ma ({TODAY_DATE}):",
            style=Pack(
                font_weight="bold",
                padding_bottom=10,
                text_align="center",
                font_size=12,
            )
        )

        self.statisztika_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                background_color="#ffffff",
                padding=10,
                width=260,
            )
        )

        jobb_panel.add(stat_cim)
        jobb_panel.add(self.statisztika_box)

        main_box.add(bal_panel)
        main_box.add(jobb_panel)

        self.main_window = toga.MainWindow(title="Pomodoro App")
        self.main_window.content = main_box

        self._build_statisztika_view()

        self._load_local_log()

        self.commands.clear()

        fajl_group = toga.Group("Fájl", order=0)
        sugo_group = toga.Group("Súgó", order=1)

        nevjegy_cmd = toga.Command(self.show_nevjegy, text="Névjegy",
                                   group=fajl_group, order=0)
        stat_export_cmd = toga.Command(
            self.on_statisztika_mentese,
            text="Statisztika mentése (CSV)",
            group=fajl_group,
            order=5,
        )
        kilepes_cmd = toga.Command(self.menu_kilepes, text="Kilépés",
                                   group=fajl_group, order=20)

        sugo_alt_cmd = toga.Command(self.sugo_altalanos, text="Általános",
                                    group=sugo_group, order=0)
        sugo_start_cmd = toga.Command(self.sugo_start_gomb, text="Start/Stop gomb",
                                      group=sugo_group, order=10)
        sugo_torles_cmd = toga.Command(self.sugo_torles_gomb, text="Törlés gomb",
                                       group=sugo_group, order=20)
        sugo_export_cmd = toga.Command(self.sugo_statisztika_mentese_gomb,
                                       text="Statisztika mentése gomb",
                                       group=sugo_group, order=30)

        self.commands.add(
            nevjegy_cmd,
            stat_export_cmd,
            kilepes_cmd,
            sugo_alt_cmd,
            sugo_start_cmd,
            sugo_torles_cmd,
            sugo_export_cmd,
        )

        self.main_window.show()


    def _block_end_alert(self, title, message):

        print(f"\n***** Hangjelzés: {title.upper()} *****\n")
        self.main_window.info_dialog(title, message)

    def _calculate_daily_summary(self):
        summary = {t: 0 for t in TANTARGYAK}
        current_date = datetime.now().strftime("%Y-%m-%d")

        for session in self.session_log:
            if session.get("date") == current_date:
                subject = session.get("subject")
                minutes = session.get("minutes", 0)
                if subject in TANTARGYAK:
                    summary[subject] += minutes

        return summary

    def _build_statisztika_view(self):

        self.statisztika_box.children.clear()
        self.statisztika_labels = {}

        fejlec = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
        fejlec.add(toga.Label("Tantárgy",
                              style=Pack(width=140, font_weight="bold", font_size=11)))
        fejlec.add(toga.Label("Idő (perc)",
                              style=Pack(font_weight="bold", font_size=11)))
        self.statisztika_box.add(fejlec)

        for index, tantargy in enumerate(TANTARGYAK):
            hatter = "#dde7ff" if index % 2 == 1 else "#ffffff"

            sor = toga.Box(
                style=Pack(
                    direction=ROW,
                    padding=2,
                    padding_left=6,
                    padding_right=6,
                    background_color=hatter,
                )
            )
            sor.add(toga.Label(tantargy, style=Pack(width=140, font_size=11)))

            perc_label = toga.Label("0 perc", style=Pack(font_size=11))
            sor.add(perc_label)

            self.statisztika_box.add(sor)
            self.statisztika_labels[tantargy] = perc_label

    def _frissit_statisztika_box(self):

        self.daily_summary = self._calculate_daily_summary()

        for tantargy, perc_label in self.statisztika_labels.items():
            perc = self.daily_summary.get(tantargy, 0)
            perc_label.text = f"{perc} perc"

    def _save_local_log(self):

        save_path = self.paths.data / LOCAL_STAT_FILE
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(self.session_log, f, indent=4, ensure_ascii=False)
            print(f"Teljes napló sikeresen mentve: {save_path}")
        except Exception as e:
            print(f"Hiba a lokális napló mentésekor: {e}")

    def _load_local_log(self):

        load_path = self.paths.data / LOCAL_STAT_FILE
        if load_path.exists():
            try:
                with open(load_path, "r", encoding="utf-8") as f:
                    loaded_data = json.load(f)
                    if isinstance(loaded_data, list):
                        self.session_log = loaded_data
                        print(f"Napló betöltve ({len(self.session_log)} bejegyzés).")
                    else:
                        print("A betöltött adat nem lista, üres naplóval indulunk.")
                        self.session_log = []
            except Exception as e:
                print(f"Hiba a napló betöltésekor: {e}")
                self.session_log = []

        self._frissit_statisztika_box()

    def _export_to_csv(self):

        if not self.session_log:
            self.main_window.info_dialog("Mentés", "Nincs elmenthető tanulási adat a naplóban.")
            return

        osszegzett = {}  # kulcs: (date, subject)  érték: perc
        for entry in self.session_log:
            date = entry.get("date")
            subject = entry.get("subject")
            minutes = entry.get("minutes", 0)

            if not date or not subject:
                continue

            key = (date, subject)
            if key not in osszegzett:
                osszegzett[key] = 0
            osszegzett[key] += minutes

        try:
            with open(CSV_EXPORT_FILE, "w", newline="", encoding="utf-8-sig") as csvfile:
                fieldnames = ["date", "subject", "minutes"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

                writer.writerow({"date": "Dátum", "subject": "Tantárgy", "minutes": "Tanult percek"})

                for (date, subject) in sorted(osszegzett.keys()):
                    writer.writerow({
                        "date": date,
                        "subject": subject,
                        "minutes": osszegzett[(date, subject)]
                    })

            self.main_window.info_dialog(
                "Mentés sikeres!",
                f"A teljes tanulási napló elmentve:\n{CSV_EXPORT_FILE}",
            )

        except PermissionError:
            self.main_window.error_dialog(
                "Mentés sikertelen",
                (
                    "Nem sikerült a mentés, mert a fájl valószínűleg meg van nyitva "
                    "(például Excelben).\n\n"
                    "Zárd be a fájlt, majd próbáld újra a mentést."
                ),
            )

        except Exception as e:
            self.main_window.error_dialog("Hiba", f"Nem sikerült a mentés:\n{e}")

    def tick(self):
        if not self.is_running:
            return

        self.loop.call_later(1.0, self.tick)

        if self.minutes == 0 and self.seconds == 0:
            if not self.is_break:

                tantargy = self.tantargy_valaszto.value
                entry = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "subject": tantargy,
                    "minutes": MUNKA_PERCEK,
                }
                self.session_log.append(entry)
                self.pomodoro_cycle += 1

                print(f"Mentve: +{MUNKA_PERCEK} perc a(z) {tantargy} tantárgyhoz. Ciklus: {self.pomodoro_cycle}")

                self._block_end_alert(
                    "Figyelem! Szünet jön!",
                    f"Vége a(z) {tantargy} tanulásának.\n"
                    f"Indul a(z) "
                    f"{SZUNET_PERCEK if self.pomodoro_cycle % 4 != 0 else HOSSZU_SZUNET_PERCEK} "
                    f"perces szünet!",
                )

                self.is_break = True
                self.beallit_szunet_idot()
            else:
                self._block_end_alert(
                    "Figyelem! Tanulás jön!",
                    f"Vége a szünetnek.\nIndul az új {MUNKA_PERCEK} perces tanulási blokk "
                    f"a(z) {self.tantargy_valaszto.value} tantárgyból!",
                )
                self.is_break = False
                self.beallit_munka_idot()

            self._save_local_log()
            self._frissit_statisztika_box()
            self.frissit_ido_label()
            self.frissit_szin()
            return

        if self.seconds == 0:
            self.minutes -= 1
            self.seconds = 59
        else:
            self.seconds -= 1

        self.frissit_ido_label()

    def on_statisztika_mentese(self, widget):
        print("Statisztika mentése gomb megnyomva.")
        self._save_local_log()
        self._export_to_csv()

    def on_start_stop_gomb(self, widget):
        if self.is_running:
            self.is_running = False
            self.start_stop_button.text = "Start"
            print("Időzítő megállítva.")
            self.main_window.info_dialog("Megállítva", "Az időzítő szünetel.")
        else:
            self.is_running = True
            self.start_stop_button.text = "Stop"
            print(f"Időzítő elindítva a(z) {self.tantargy_valaszto.value} tantárgyhoz.")
            self.loop.call_later(1.0, self.tick)

        self._frissit_statisztika_box()

    def on_reset_gomb(self, widget):
        print("Törlés gomb megnyomva.")
        self.is_running = False
        self.is_break = False
        self.pomodoro_cycle = 0
        self.start_stop_button.text = "Start"
        self.beallit_munka_idot()
        self.frissit_ido_label()
        self.frissit_szin()

        self.main_window.info_dialog(
            "Időzítő törölve",
            f"Az időzítő leállt és visszaállt tanulási módra ({MUNKA_PERCEK:02d}:00).",
        )

        self._frissit_statisztika_box()

    def sugo_altalanos(self, widget):
        self.main_window.info_dialog(
            "Súgó – Általános",
            (
                "A Pomodoro-módszer egy tanulási technika, amely az időt\n"
                "kisebb, fókuszált szakaszokra bontja.\n"
                f"{MUNKA_PERCEK} perc tanulás – {SZUNET_PERCEK} perc szünet váltakozik minden"
                f"négyszer, majd egy hosszabb ({HOSSZU_SZUNET_PERCEK} perces) szünet következik.\n\n"
                "Segít koncentráltan tanulni, javítja a teljesítményt és\n"
                "megakadályozza a kifáradást.\n\n"
                "Válaszd ki a tantárgyat, indítsd el az időzítőt a Start/Stop gombbal, "
                "és tanulj, amíg ketyeg az óra."
            ),
        )

    def sugo_start_gomb(self, widget):
        self.main_window.info_dialog(
            "Súgó – Start/Stop gomb",
            (
                "A Start/Stop gombbal tudod elindítani, illetve megállítani\n"
                "az aktuális tanulási vagy szünet blokkot.\n\n"
                "Ha megállítod, a számláló ott marad, ahol tartottál, amíg újra el nem indítod."
            ),
        )

    def sugo_torles_gomb(self, widget):
        self.main_window.info_dialog(
            "Súgó – Törlés gomb",
            (
                f"A Törlés gombbal tudod visszaállítani az időzítőt az alapértékre ({MUNKA_PERCEK:02d}:00). "
                "Ezzel visszaváltasz tanulási módba, és lenullázod a számlálót.\n\n"
                "A napi statisztika adatait NEM törlöd, csak az órát állítod vissza vele."
            ),
        )

    def sugo_statisztika_mentese_gomb(self, widget):
        self.main_window.info_dialog(
            "Súgó – Statisztika mentése gomb",
            (
                "A „Statisztika mentése” gomb a teljes tanulási naplót\n"
                "elmenti egy Excelben is megnyitható fájlba.\n\n"
                "Az összes addig tanult időd mentésre kerül napokra és tantárgyakra bontva.\n"
                "Ha egy nap egy tárgyból többször is tanulsz 25 percet, akkor összesíti neked a tanult perceket."
            ),
        )

    def menu_kilepes(self, widget):

        self._save_local_log()
        self.exit()

    def show_nevjegy(self, widget):

        self.main_window.info_dialog(
            "Névjegy",
            (
                "Pomodoro App – Verzió: 1.0\n\n"
                "A Pomodoro App egy hatékony tanulást segítő alkalmazás.\n"
                "Célja, hogy segítsen a tanulóknak jobban beosztani az idejüket,"
                "fenntartani a figyelmet, és visszajelzést adni a napi tanulási teljesítményükről.\n\n"
                "Készítette: Suba-Kiss Beáta\n"
                "Készült: 2025"
            ),
        )

def main():
    return PomodoroApp("Pomodoro", "hu.subabea.pomodoro")

if __name__ == "__main__":
    app = main()
    app.main_loop()

