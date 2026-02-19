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

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Search a champion (Aatrox, Garen, etc.).", width=400)
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
        if hasattr(self, "credit"): self.credit.pack_forget()

        self.details_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.details_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.details_frame.grid_columnconfigure(0, weight=1) 
        self.details_frame.grid_columnconfigure(1, weight=3)
        self.details_frame.grid_rowconfigure(0, weight=0)
        self.details_frame.grid_rowconfigure(1, weight=1)

        self.btn_return = customtkinter.CTkButton(
            self.details_frame, 
            text="Return", # Seta para indicar voltar
            command=self.return_button, 
            fg_color="transparent", 
            width=50, # Largura compacta
            anchor="w" # Texto alinhado a esquerda
        )
        self.btn_return.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 10))

        self.left_panel = customtkinter.CTkFrame(self.details_frame, fg_color="#2B2B2B", corner_radius=15)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.left_content = customtkinter.CTkFrame(self.left_panel, fg_color="transparent")
        self.left_content.pack(expand=True, fill="both", pady=20)

        self.right_panel = customtkinter.CTkFrame(self.details_frame, fg_color="#2B2B2B", corner_radius=15)
        self.right_panel.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=(0, 10))
        self.right_content = customtkinter.CTkFrame(self.left_panel, fg_color="transparent")
        self.right_content.pack(expand=True, fill="both", pady=40)

        # Gathering info --------------------------------------------------------------

        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_matchups = self.load_data()
        img = self.data_matchups.get(champ_name, {}).get("img")
        icons_path = os.path.join(script_dir, "icons", img)
        if os.path.exists(icons_path):
            pil_image = Image.open(icons_path)
            self.my_image = customtkinter.CTkImage(
                light_image=pil_image, 
                dark_image=pil_image, 
                size=(100, 100) 
            )
            self.img_label = customtkinter.CTkLabel(self.left_content, text="", image=self.my_image)
            self.img_label.pack(pady=(0, 15))
        else:
            print(f"Imagem não encontrada: {icons_path}")

        diff = data_matchups.get(champ_name, {}).get("difficulty", "Unknown")
        runes = data_matchups.get(champ_name, {}).get("runes", "Conqueror")
        notes = data_matchups.get(champ_name, {}).get("notes", "No notes yet.")
        todo = data_matchups.get(champ_name, {}).get("todo", "No notes yet.")
        nottodo = data_matchups.get(champ_name, {}).get("nottodo", "No notes yet.")
        item = data_matchups.get(champ_name, {}).get("start-item", "")
        item_icon = os.path.join(script_dir, "icons", item)

        # ------------------------------------------------------------------------------

        self.entry.pack_forget()
        self.scroll_frame.pack_forget()

        champion_name = customtkinter.CTkLabel(self.left_content, text=champ_name, font=("Arial", 26))
        champion_name.pack(pady=(0, 15)) 

        lbl_items_title = customtkinter.CTkLabel(self.left_content, text="Recommended Items", font=("Arial", 18, "bold"), anchor="w")
        lbl_items_title.pack(fill="x", pady=(10, 5))

        items_card = customtkinter.CTkFrame(self.left_content, fg_color="#333333")
        items_card.pack(fill="x", pady=5)

        start_items = data_matchups.get(champ_name, {}).get("start-items", [])

        self.item_images = []

        if not start_items:
            lbl = customtkinter.CTkLabel(items_card, text="Not defined", font=("Arial", 14))
            lbl.pack(pady=10, padx=15, anchor="w")
        else:
            items_container = customtkinter.CTkFrame(items_card, fg_color="transparent")
            items_container.pack(pady=10, padx=15, anchor="w")
            for item in start_items:
                item_name = item.get("name", "Unknown Item")
                item_img_name = item.get("img", "")
                item_icon_path = os.path.join(script_dir, "icons", item_img_name)

                if item_img_name and os.path.exists(item_icon_path):
                    pil_image_item = Image.open(item_icon_path)
                    ctk_img = customtkinter.CTkImage(
                        light_image=pil_image_item, 
                        dark_image=pil_image_item, 
                        size=(50, 50) 
                    )
                    self.item_images.append(ctk_img) 
                    lbl = customtkinter.CTkLabel(items_container, text=f" {item_name}", image=ctk_img, compound="left", font=("Arial", 14))
                    lbl.pack(side="left", padx=(10, 10)) 
                else:
                    lbl = customtkinter.CTkLabel(items_container, text=item_name, font=("Arial", 14))
                    lbl.pack(side="left", padx=(10, 10))

        lbl_runes_title = customtkinter.CTkLabel(self.right_panel, text="Recommended Runes", font=("Arial", 18, "bold"), anchor="w")
        lbl_runes_title.pack(fill="x", pady=(10, 5))

        rune_card = customtkinter.CTkFrame(self.right_panel, fg_color="#333333")
        rune_card.pack(fill="x", pady=5)
        
        lbl_runes = customtkinter.CTkLabel(rune_card, text=runes, font=("Arial", 14), anchor="w", justify="left")
        lbl_runes.pack(padx=15, pady=15, fill="x")

        lbl_notes_title = customtkinter.CTkLabel(self.right_panel, text="Matchup Notes", font=("Arial", 18, "bold"), anchor="w")
        lbl_notes_title.pack(fill="x", pady=(20, 5))

        lbl_notes = customtkinter.CTkLabel(self.right_panel, text=notes, font=("Arial", 14), wraplength=500, justify="left", anchor="w")
        lbl_notes.pack(fill="x", pady=5)

        lbl_todo_title = customtkinter.CTkLabel(self.right_panel, text="To do:", font=("Arial", 18, "bold"), anchor="w")
        lbl_todo_title.pack(fill="x", pady=(20, 5))

        lbl_todo = customtkinter.CTkLabel(self.right_panel, text=todo, font=("Arial", 14), wraplength=500, justify="left", anchor="w")
        lbl_todo.pack(fill="x", pady=5)

        lbl_nottodo_title = customtkinter.CTkLabel(self.right_panel, text="Don't:", font=("Arial", 18, "bold"), anchor="w")
        lbl_nottodo_title.pack(fill="x", pady=(20, 5))

        lbl_nottodo = customtkinter.CTkLabel(self.right_panel, text=nottodo, font=("Arial", 14), wraplength=500, justify="left", anchor="w")
        lbl_nottodo.pack(fill="x", pady=5)

    def return_button(self):
        if hasattr(self, 'details_frame'):
            self.details_frame.destroy()
        self.setup_menu()
        self.champions_grid()
        


if __name__ == "__main__":
    app = RivenNation()
    app.mainloop()





