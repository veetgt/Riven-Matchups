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
        self.setup_ui()
        self.champions_grid()

    def load_data(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(script_dir, "matchups.json")

        if os.path.exists(json_dir):
            try:
                with open("matchups.json", "r", encoding="utf-8") as something:
                    return json.load(something)
            except Exception as e:
                print(f"Erro no JSON: {e}")
                return {}
        
    def setup_ui(self):
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
            icons_path = os.path.join(script_dir, "images", self.data_matchups[champion]["img"])
            img_btn = None

            if os.path.exists(icons_path):
                try:
                    img_data = Image.open(icons_path)
                    img_btn = customtkinter.CTkImage(light_image=img_data, 
                                                    dark_image=img_data, 
                                                    size=(55, 55))
                except Exception as e:
                    print(f"Image error {champion}: {e}")
            
            btn = customtkinter.CTkButton(
                self.scroll_frame, 
                text=champion,
                command=lambda c=champion: self.button_event(c), 
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

    def button_event(self, champ_name):
        print(f"{champ_name}")

if __name__ == "__main__":
    app = RivenNation()
    app.mainloop()





