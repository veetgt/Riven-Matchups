import customtkinter
from PIL import Image
import json
import os

class RivenNation(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Riven Matchup Guide")       
        self.geometry("854x480")
        customtkinter.set_appearance_mode("dark")
        self.data_matchups = self.load_data()
        self.setup_menu()
        self.champions_grid()

    def load_data(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(script_dir, "matchups.json")

        if os.path.exists(json_dir):
            try:
                with open(json_dir, "r", encoding="utf-8") as something:
                    return json.load(something)
            except Exception as e:
                print(f"Erro no JSON: {e}")
                return {}
        
    def setup_menu(self):
        self.credit = customtkinter.CTkLabel(master=self, text="by VeetGoodtime", font=("Arial", 9))
        self.credit.pack(pady=8)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Choose a champion (Aatrox, Garen, etc.).", width=400)
        self.entry.pack(pady=3)

        self.scroll_frame = customtkinter.CTkScrollableFrame(master=self, width=480, height=320)
        self.scroll_frame.pack(pady=20)

    def champions_grid(self, filter=None):
        COLUMN_LIMIT = 6
        row = 0
        column = 0 
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        champions = list(self.data_matchups.keys())

        for champion in champions:
            icons_path = os.path.join(script_dir, "icons", self.data_matchups[champion]["img"])
            img_btn = None

            if os.path.exists(icons_path):
                try:
                    img_btn = customtkinter.CTkImage(light_image=Image.open(icons_path), 
                                                    dark_image=Image.open(icons_path), 
                                                    size=(55, 55))
                except Exception as e:
                    print(f"Image error {champion}: {e}")
            
            btn = customtkinter.CTkButton(
                self.scroll_frame, 
                text=champion,
                command=lambda c=champion: self.champion_select(c), 
                width=0, height=0,
                compound="top",
                image=img_btn,
                anchor="center",
                fg_color="transparent",
                hover_color="#404040")
            
            btn.grid(row=row, column=column, padx=3, pady=3)
            column += 1
            if column >= COLUMN_LIMIT:
                column = 0
                row += 1
        
    def champion_select(self, champ_name): # New window
        print(f"{champ_name}")

        # Gathering info
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_matchups = self.load_data()
        img = self.data_matchups.get(champ_name, {}).get("img")
        icons_path = os.path.join(script_dir, "icons", img)
        if os.path.exists(icons_path):
            pil_image = Image.open(icons_path)
            self.my_image = customtkinter.CTkImage(
                light_image=pil_image, 
                dark_image=pil_image, 
                size=(70, 70) 
            )
            self.img_label = customtkinter.CTkLabel(master=self, text="", image=self.my_image)
            self.img_label.pack(pady=10)
        else:
            print(f"Imagem não encontrada: {icons_path}")

        diff = data_matchups.get(champ_name, {}).get("difficulty", "Unknown")
        runes = data_matchups.get(champ_name, {}).get("runes", "Conqueror")
        notes = data_matchups.get(champ_name, {}).get("notes", "No notes yet.")
        todo = data_matchups.get(champ_name, {}).get("todo", "")
        nottodo = data_matchups.get(champ_name, {}).get("nottodo", "")

        self.entry.pack_forget()
        self.scroll_frame.pack_forget()

        self.champion_name = customtkinter.CTkLabel(master=self, text=champ_name, font=("Arial", 26))
        self.champion_name.pack()

        self.diff_label = customtkinter.CTkLabel(master=self, text=f"{diff}", font=("Arial", 16))
        self.diff_label.pack(pady=5)

        self.return_btn = customtkinter.CTkButton(master=self, text="return", command=self.return_button)
        self.return_btn.pack(pady=12)

    def return_button(self):
        self.credit.pack_forget()
        self.img_label.pack_forget()
        self.champion_name.pack_forget()
        self.diff_label.pack_forget()
        self.return_btn.pack_forget()
        self.setup_menu()
        self.champions_grid()
        


if __name__ == "__main__":
    app = RivenNation()
    app.mainloop()





