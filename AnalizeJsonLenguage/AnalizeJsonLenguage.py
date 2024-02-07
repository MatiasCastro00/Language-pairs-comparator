import math
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json


class JSONLocalizationChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Localization Checker")

        self.select_file_button = tk.Button(
            self.root, text="Seleccionar Archivo JSON", command=self.select_file
        )
        self.select_file_button.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self.root, height=15, width=75)
        self.text_area.pack(pady=5)
        self.text_area.insert(tk.INSERT, "Resultados...\n")
        self.text_area.configure(state="disabled")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.process_json_file(file_path)
        else:
            messagebox.showinfo("Informacion", "No se selecciono ningun archivo.")

    def clamp(n, min, max):
        if n < min:
            return min
        elif n > max:
            return max
        else:
            return n

    def process_json_file(self, file_path):
        missing_keys_output = ""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {e}")
            return

        # Preparar _meta y maxChars
        data["_meta"] = data.get("_meta", {})
        data["_meta"]["maxChars"] = data["_meta"].get("maxChars", {})

        for key in set(data.get("en", {}).keys()) | set(data.get("es", {}).keys()):
            if key in data["en"] and key not in data["es"]:
                missing_keys_output += (
                    f'La clave "{key}" se encuentra en "EN" pero no en "ES".\n'
                )
            elif key in data["es"] and key not in data["en"]:
                missing_keys_output += (
                    f'La clave "{key}" se encuentra en "ES" pero no en "EN".\n'
                )

            # Calcular maxChars
            len_en = len(data.get("en", {}).get(key, ""))
            len_es = len(data.get("es", {}).get(key, ""))
            max_len = max(len_en, len_es)
            data["_meta"]["maxChars"][key] = int(
                max_len + min(max(max_len * 0.5, 10), 40)
            )

        self.save_json(file_path, data)
        self.update_text_area(
            missing_keys_output
            if missing_keys_output
            else "Todas las claves estan presentes en ambos idiomas."
        )

    def save_json(self, file_path, data):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            messagebox.showinfo(
                "Proceso completado", "El archivo ha sido actualizado con exito."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

    def update_text_area(self, missing_keys_output):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(
            tk.INSERT, "Resultados de la comparacion:\n\n" + missing_keys_output
        )
        self.text_area.configure(state="disabled")


def main():
    root = tk.Tk()
    JSONLocalizationChecker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
