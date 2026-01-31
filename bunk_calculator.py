import customtkinter as ctk
from math import ceil, floor

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

NEON_CYAN = "#1CA1AF"
NEON_PINK = "#FF4081"
DEEP_BG = "#121212"                     
CARD_BG = "#212020" 
TEXT_WHITE = "#FFFFFF"

class BunkCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BUNK MEE 🚀")
        self.geometry("450x650")
        self.resizable(False, False)
        self.configure(fg_color=DEEP_BG)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=0) 
        self.grid_rowconfigure(2, weight=0) 
        self.grid_rowconfigure(3, weight=0) 
        self.grid_rowconfigure(4, weight=1) 

        self.title_font = ctk.CTkFont(family="Segoe UI Black", size=36, weight="bold")
        self.label_font = ctk.CTkFont(family="Roboto Medium", size=14)
        self.result_font = ctk.CTkFont(family="Roboto", size=16, weight="bold")
        self.main_font = ctk.CTkFont(family="Roboto", size=14)

        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, pady=(40, 20))
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="BUNK MEE", 
            font=self.title_font, 
            text_color=NEON_CYAN
        )
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="MASTER YOUR ATTENDANCE",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=NEON_PINK,
            
        )
        self.subtitle_label.pack(pady=(0, 0))

        self.input_card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15, border_width=1, border_color="#333")
        self.input_card.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        self.input_card.grid_columnconfigure(0, weight=1)
        self.input_card.grid_columnconfigure(1, weight=1)

        self.present_label = ctk.CTkLabel(self.input_card, text="CLASSES ATTENDED", font=self.label_font, text_color="gray")
        self.present_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.present_entry = ctk.CTkEntry(
            self.input_card, 
            placeholder_text="0", 
            height=35,
            border_color=NEON_CYAN,
            fg_color="#2b2b2b",
            text_color="white"
        )
        self.present_entry.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.absent_label = ctk.CTkLabel(self.input_card, text="CLASSES MISSED", font=self.label_font, text_color="gray")
        self.absent_label.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="w")
        self.absent_entry = ctk.CTkEntry(
            self.input_card, 
            placeholder_text="0", 
            height=35,
            border_color=NEON_PINK,
            fg_color="#2b2b2b",
            text_color="white"
        )
        self.absent_entry.grid(row=1, column=1, padx=20, pady=(0, 15), sticky="ew")

        self.threshold_label = ctk.CTkLabel(self.input_card, text="TARGET PERCENTAGE (%)", font=self.label_font, text_color="gray")
        self.threshold_label.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 5), sticky="w")
        self.threshold_entry = ctk.CTkEntry(
            self.input_card, 
            placeholder_text="75", 
            height=35,
            border_color="#555",
            fg_color="#2b2b2b",
            text_color="white"
        )
        self.threshold_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 25), sticky="ew")
        self.threshold_entry.insert(0, "75")

        self.calculate_button = ctk.CTkButton(
            self, 
            text="CALCULATE FATE", 
            command=self.calculate_attendance,
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            height=50,
            fg_color=NEON_CYAN,
            text_color="black",
            hover_color="#00B8D4",
            corner_radius=25
        )
        self.calculate_button.grid(row=2, column=0, padx=50, pady=30, sticky="ew")

        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame.grid(row=3, column=0, padx=20, pady=0, sticky="ew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.progress_label = ctk.CTkLabel(self.result_frame, text="CURRENT ATTENDANCE", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray")
        self.progress_label.grid(row=0, column=0, pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.result_frame, height=15, corner_radius=10, progress_color=NEON_CYAN)
        self.progress_bar.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        self.perc_label = ctk.CTkLabel(self.result_frame, text="0%", font=ctk.CTkFont(family="Segoe UI", size=48, weight="bold"), text_color=NEON_CYAN)
        self.perc_label.grid(row=2, column=0, pady=0)

        self.advice_label = ctk.CTkLabel(self.result_frame, text="Enter your stats above.", font=self.main_font, text_color="gray",wraplength=380, justify="center")
        self.advice_label.grid(row=3, column=0, pady=10)


    def calculate_attendance(self):
        try:
            present_val = self.present_entry.get()
            absent_val = self.absent_entry.get()
            threshold_val = self.threshold_entry.get()

            if not present_val or not absent_val:
                self.advice_label.configure(text="Please fill in all fields!", text_color=NEON_PINK)
                return

            present = int(present_val)
            absent = int(absent_val)
            threshold = float(threshold_val) if threshold_val else 75.0

            total = present + absent
            if total == 0:
                self.advice_label.configure(text="You haven't had any classes yet!", text_color="white")
                return

            current_percentage = (present / total) * 100
            
            self.progress_bar.set(current_percentage / 100)
            self.perc_label.configure(text=f"{current_percentage:.1f}%")
            
            if current_percentage < threshold:
                self.progress_bar.configure(progress_color=NEON_PINK)
                self.perc_label.configure(text_color=NEON_PINK)
            else:
                self.progress_bar.configure(progress_color=NEON_CYAN)
                self.perc_label.configure(text_color=NEON_CYAN)


            if current_percentage >= threshold:
                if threshold == 0:
                     bunkable = 999
                else:
                    bunkable = floor((present * 100) / threshold - total)
                
                if bunkable <= 0:
                     self.advice_label.configure(text=f"You are safe, but ON THE EDGE. Don't bunk!", text_color="#F1FA8C")
                else:
                    self.advice_label.configure(text=f"You can safely bunk {bunkable} classes 🥳", text_color=NEON_CYAN)
            else:
                if threshold >= 100: 
                     if absent > 0:
                         self.advice_label.configure(text="It's impossible to reach 100% now. RIP.", text_color=NEON_PINK)
                         return
                     else:
                        needed = 0
                else:
                    needed = ceil((threshold * total - 100 * present) / (100 - threshold))
                
                if needed <= 0:
                    self.advice_label.configure(text="You're actually fine!", text_color=NEON_CYAN)
                else:
                    self.advice_label.configure(text=f"WARNING: You must attend {needed} classes straight! 🚨", text_color=NEON_PINK)

        except ValueError:
             self.advice_label.configure(text="Invalid numbers entered.", text_color=NEON_PINK)

if __name__ == "__main__":
    app = BunkCalculatorApp()
    app.mainloop()
