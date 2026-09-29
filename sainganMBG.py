import tkinter as tk
from tkinter import ttk, messagebox
print("🔥 THIS IS THE NEW SAINGANMBG FILE 🔥")
FOODS = [
    {"no": 1, "name": "Mie Ayam", "energy": 102, "protein": 6.2, "fat": 3.9, "fiber": 0, "sodium": 279, "vegetarian": False, "allergens": ["gluten", "telur", "kedelai"]},
    {"no": 2, "name": "Nasi Rames", "energy": 155, "protein": 10.3, "fat": 4.2, "fiber": 0, "sodium": 255, "vegetarian": False, "allergens": ["kedelai", "telur"]},
    {"no": 3, "name": "Ayam Goreng Kalasan, paha", "energy": 298, "protein": 34.2, "fat": 16.6, "fiber": 0, "sodium": 141, "vegetarian": False, "allergens": ["kedelai", "gluten"]},
    {"no": 4, "name": "Beef Teriyaki", "energy": 151, "protein": 8.5, "fat": 3.1, "fiber": 0.3, "sodium": 377, "vegetarian": False, "allergens": ["kedelai", "gluten"]},
    {"no": 5, "name": "Gulai Kambing", "energy": 126, "protein": 4.2, "fat": 9.4, "fiber": 0, "sodium": 302, "vegetarian": False, "allergens": ["susu"]},
    {"no": 6, "name": "Sop Buntut", "energy": 71, "protein": 7.5, "fat": 3.6, "fiber": 0, "sodium": 490, "vegetarian": False, "allergens": ["kedelai"]},
    {"no": 7, "name": "Sop Konro", "energy": 71, "protein": 7.4, "fat": 2.6, "fiber": 0, "sodium": 18, "vegetarian": False, "allergens": ["kedelai"]},
    {"no": 8, "name": "Soto Madura", "energy": 60, "protein": 3.5, "fat": 4.5, "fiber": 0, "sodium": 0, "vegetarian": False, "allergens": ["kedelai"]},
    {"no": 9, "name": "Soto Padang", "energy": 84, "protein": 3.0, "fat": 6.8, "fiber": 0.3, "sodium": 0, "vegetarian": False, "allergens": ["kedelai", "gluten"]},
    {"no": 10, "name": "Cumi Goreng", "energy": 265, "protein": 40.6, "fat": 10.1, "fiber": 0, "sodium": 66, "vegetarian": False, "allergens": ["moluska", "gluten"]},
    {"no": 11, "name": "Telur Ayam Dadar", "energy": 251, "protein": 16.3, "fat": 19.4, "fiber": 0, "sodium": 0, "vegetarian": True, "allergens": ["telur"]},
    {"no": 12, "name": "Rendang Sapi", "energy": 193, "protein": 22.5, "fat": 7.9, "fiber": 0, "sodium": None, "vegetarian": False, "allergens": []},
    {"no": 13, "name": "Ketoprak", "energy": 153, "protein": 7.9, "fat": 7.7, "fiber": 2.9, "sodium": 0, "vegetarian": True, "allergens": ["kacang", "kedelai"]},
    {"no": 14, "name": "Bubur Manado", "energy": 156, "protein": 2.3, "fat": 0.2, "fiber": 8.2, "sodium": 460, "vegetarian": True, "allergens": []},
    {"no": 15, "name": "Spageti", "energy": 138, "protein": 7.4, "fat": 2.1, "fiber": 0, "sodium": 0, "vegetarian": False, "allergens": ["gluten", "telur", "susu"]},
    {"no": 16, "name": "Pepes Oncom Ampas Tahu", "energy": 75, "protein": 5.2, "fat": 1.8, "fiber": 22, "sodium": 0, "vegetarian": True, "allergens": ["kedelai"]},
    {"no": 17, "name": "Tahu Goreng", "energy": 115, "protein": 8.7, "fat": 8.5, "fiber": 0.1, "sodium": 1, "vegetarian": True, "allergens": ["kedelai", "gluten"]},
    {"no": 18, "name": "Sayur Bayam", "energy": 23, "protein": 1.2, "fat": 0.6, "fiber": 1.1, "sodium": 16, "vegetarian": True, "allergens": []},
    {"no": 19, "name": "Gado-gado", "energy": 137, "protein": 6.1, "fat": 22, "fiber": 1.1, "sodium": 0, "vegetarian": True, "allergens": ["kacang", "kedelai"]},
    {"no": 20, "name": "Rujak Cingur", "energy": 153, "protein": 11.3, "fat": 8.4, "fiber": 1.4, "sodium": 0, "vegetarian": False, "allergens": ["kacang", "kedelai"]},
]

ALLERGIES = [
    "Tidak ada", "Gluten", "Telur", "Kedelai", "Susu",
    "Kacang", "Ikan", "Udang", "Moluska"
]

"""
Q1 energy  = 81.75 kcal
Median energy = 137.50 kcal
Q3 energy  = 155.25 kcal
Median protein = 7.45 g
Q3 protein = 10.55 g
"""
LOW_ENERGY = 82
HIGH_ENERGY = 155
MEDIAN_PROTEIN = 7.45
HIGH_PROTEIN = 10.55
FIBER_RICH = 1.0
MODERATE_FAT = 5.65

"""
FORWARD-CHAINING RULES
R1  Vegetarian match
R2  Allergy safe
R3  Optional calorie constraint
Goal rules:
R4  Menurunkan:
    low-energy AND (adequate-protein OR fiber-rich)
    AND moderate-fat
R5  Menaikkan:
    high-energy AND high-protein
R6  Menjaga:
    moderate-energy AND adequate-protein
R7  Final recommendation:
    vegetarian_match AND allergy_safe AND calorie_match
    AND goal_match

Note: R4-R6 are dataset-relative prototype rules. They are not universal medical thresholds.
"""

def contains_allergen(food, allergy):
    if allergy == "Tidak ada":
        return False
    return allergy.lower() in [a.lower() for a in food["allergens"]]


def forward_chain(food, goal, vegetarian_user, max_calories, allergy):
    facts = set()
    trace = []

    #R1: dietary preference
    if (not vegetarian_user) or food["vegetarian"]:
        facts.add("vegetarian_match")
        trace.append(
            "R1 FIRED: vegetarian user cocok dengan makanan."
        )

    #R2: allergy safety
    if not contains_allergen(food, allergy):
        facts.add("allergy_safe")
        trace.append(
            "R2 FIRED: makanan tidak mengandung alergen yang dipilih."
        )

    #R3: optional calorie constraint
    if max_calories is None or food["energy"] <= max_calories:
        facts.add("calorie_match")
        if max_calories is None:
            trace.append(
                "R3 FIRED: batas kalori kosong -> filter kalori dilewati."
            )
        else:
            trace.append(
                f"R3 FIRED: {food['energy']} <= {max_calories} kcal."
            )

    #Derived facts used by goal rules
    if food["energy"] <= LOW_ENERGY:
        facts.add("low_energy")
        trace.append(
            f"F1 DERIVED: low_energy ({food['energy']} <= {LOW_ENERGY})."
        )

    if food["energy"] >= HIGH_ENERGY:
        facts.add("high_energy")
        trace.append(
            f"F2 DERIVED: high_energy ({food['energy']} >= {HIGH_ENERGY})."
        )

    if LOW_ENERGY < food["energy"] < HIGH_ENERGY:
        facts.add("moderate_energy")
        trace.append(
            f"F3 DERIVED: moderate_energy ({LOW_ENERGY} < {food['energy']} < {HIGH_ENERGY})."
        )

    if food["protein"] >= MEDIAN_PROTEIN:
        facts.add("adequate_protein")
        trace.append(
            f"F4 DERIVED: adequate_protein ({food['protein']} >= {MEDIAN_PROTEIN} g)."
        )

    if food["protein"] >= HIGH_PROTEIN:
        facts.add("high_protein")
        trace.append(
            f"F5 DERIVED: high_protein ({food['protein']} >= {HIGH_PROTEIN} g)."
        )

    if food["fiber"] >= FIBER_RICH:
        facts.add("fiber_rich")
        trace.append(
            f"F6 DERIVED: fiber_rich ({food['fiber']} >= {FIBER_RICH} g)."
        )

    if food["fat"] <= MODERATE_FAT:
        facts.add("moderate_fat")
        trace.append(
            f"F7 DERIVED: moderate_fat ({food['fat']} <= {MODERATE_FAT} g)."
        )

    #R4: weight loss / lower-energy choice
    if (
        goal == "Menurunkan"
        and "low_energy" in facts
        and ("adequate_protein" in facts or "fiber_rich" in facts)
        and "moderate_fat" in facts
    ):
        facts.add("goal_match")
        trace.append(
            "R4 FIRED: tujuan MENURUNKAN cocok "
            "(low_energy + protein/fiber + moderate_fat)."
        )

    #R5: weight gain / higher-energy + protein choice
    if (
        goal == "Menaikkan"
        and "high_energy" in facts
        and "high_protein" in facts
    ):
        facts.add("goal_match")
        trace.append(
            "R5 FIRED: tujuan MENAIKKAN cocok "
            "(high_energy + high_protein)."
        )

    #R6: maintain / middle-energy + adequate protein
    if (
        goal == "Menjaga"
        and "moderate_energy" in facts
        and "adequate_protein" in facts
    ):
        facts.add("goal_match")
        trace.append(
            "R6 FIRED: tujuan MENJAGA cocok "
            "(moderate_energy + adequate_protein)."
        )

    #R7: final rule
    if {
        "vegetarian_match",
        "allergy_safe",
        "calorie_match",
        "goal_match",
    }.issubset(facts):
        facts.add("recommended")
        trace.append(
            "R7 FIRED: SEMUA kondisi terpenuhi -> DIREKOMENDASIKAN."
        )
    else:
        facts.add("not_recommended")

    return facts, trace


def recommend(goal, vegetarian_user, max_calories, allergy):
    results = []

    for food in FOODS:
        facts, trace = forward_chain(
            food,
            goal,
            vegetarian_user,
            max_calories,
            allergy
        )

        if "recommended" in facts:
            # Ranking is NOT the inference mechanism.
            # It only orders foods that already passed R7.
            score = (
                food["protein"] * 2
                + food["fiber"]
                - food["fat"] * 0.25
            )
            results.append({
                "food": food,
                "facts": facts,
                "trace": trace,
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("sainganMBG")
        self.root.geometry("1150x760")
        self.root.minsize(1000, 680)
        self.window.configure(bg="#F7F8F5")

        ttk.Label(
            root,
            text="Makan Apa Yah Hari Ini?",
            font=("Poppins", 21, "bold")
        ).pack(pady=(14, 2))

        ttk.Label(
            root,
            text="Knowledge-Based System - Forward Chaining",
            font=("Poppins", 11)
        ).pack(pady=(0, 10))

        form = ttk.LabelFrame(root, text="Input Pengguna", padding=12)
        form.pack(fill="x", padx=20, pady=5)

        ttk.Label(form, text="Tujuan:").grid(
            row=0, column=0, sticky="w", padx=5, pady=6
        )
        self.goal_var = tk.StringVar(value="Menjaga")
        ttk.Combobox(
            form,
            textvariable=self.goal_var,
            values=["Menurunkan", "Menaikkan", "Menjaga"],
            state="readonly",
            width=20
        ).grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(form, text="Vegetarian:").grid(
            row=0, column=2, sticky="w", padx=5, pady=6
        )
        self.veg_var = tk.StringVar(value="Tidak")
        ttk.Combobox(
            form,
            textvariable=self.veg_var,
            values=["Tidak", "Ya"],
            state="readonly",
            width=20
        ).grid(row=0, column=3, padx=5, pady=6)

        ttk.Label(form, text="Batas kalori (opsional):").grid(
            row=1, column=0, sticky="w", padx=5, pady=6
        )
        self.cal_var = tk.StringVar()
        ttk.Entry(
            form, textvariable=self.cal_var, width=23
        ).grid(row=1, column=1, padx=5, pady=6)

        ttk.Label(form, text="Alergi:").grid(
            row=1, column=2, sticky="w", padx=5, pady=6
        )
        self.allergy_var = tk.StringVar(value="Tidak ada")
        ttk.Combobox(
            form,
            textvariable=self.allergy_var,
            values=ALLERGIES,
            state="readonly",
            width=20
        ).grid(row=1, column=3, padx=5, pady=6)

        ttk.Button(
            form,
            text="CARI REKOMENDASI",
            command=self.run
        ).grid(
            row=0, column=4, rowspan=2,
            padx=25, ipadx=15, ipady=8
        )

        result_frame = ttk.LabelFrame(
            root, text="Hasil Forward Chaining", padding=10
        )
        result_frame.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        columns = (
            "Makanan", "Kalori", "Protein", "Lemak",
            "Serat", "Vegetarian", "Alergen"
        )

        self.tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=12
        )

        widths = [230, 80, 80, 80, 80, 100, 230]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(
                col, width=width, anchor="center"
            )

        yscroll = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(
            yscrollcommand=yscroll.set
        )

        self.tree.pack(
            side="left", fill="both", expand=True
        )
        yscroll.pack(side="right", fill="y")

        trace_frame = ttk.LabelFrame(
            root, text="Trace / Jejak Inference", padding=8
        )
        trace_frame.pack(
            fill="both", padx=20, pady=(0, 15)
        )

        self.trace = tk.Text(
            trace_frame,
            height=10,
            wrap="word"
        )
        self.trace.pack(fill="both", expand=True)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.show_trace
        )

        self.result_data = []

    def run(self):
        goal = self.goal_var.get()
        vegetarian_user = self.veg_var.get() == "Ya"
        allergy = self.allergy_var.get()

        raw_cal = self.cal_var.get().strip()

        if raw_cal == "":
            max_calories = None
        else:
            try:
                max_calories = float(raw_cal)
                if max_calories <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Input tidak valid",
                    "Batas kalori harus berupa angka positif "
                    "atau dikosongkan."
                )
                return

        self.result_data = recommend(
            goal,
            vegetarian_user,
            max_calories,
            allergy
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.trace.delete("1.0", tk.END)

        for index, item in enumerate(self.result_data):
            food = item["food"]

            allergen_text = (
                ", ".join(food["allergens"])
                if food["allergens"] else "-"
            )

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    food["name"],
                    food["energy"],
                    food["protein"],
                    food["fat"],
                    food["fiber"],
                    "Ya" if food["vegetarian"] else "Tidak",
                    allergen_text
                )
            )

        if not self.result_data:
            self.trace.insert(
                tk.END,
                "Tidak ada makanan yang memenuhi semua rule.\n\n"
                "Coba ubah tujuan, batas kalori, atau filter alergi."
            )
        else:
            self.trace.insert(
                tk.END,
                f"Ditemukan {len(self.result_data)} makanan.\n"
                "Klik makanan untuk melihat fakta dan rule "
                "yang terpicu."
            )

    def show_trace(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        index = int(selected[0])
        item = self.result_data[index]
        food = item["food"]

        self.trace.delete("1.0", tk.END)

        self.trace.insert(
            tk.END,
            f"MAKANAN: {food['name']}\n"
        )
        self.trace.insert(
            tk.END,
            "=" * 65 + "\n\n"
        )

        self.trace.insert(
            tk.END,
            "FAKTA DARI DATASET:\n"
        )
        self.trace.insert(
            tk.END,
            f"- Energi: {food['energy']} kcal\n"
        )
        self.trace.insert(
            tk.END,
            f"- Protein: {food['protein']} g\n"
        )
        self.trace.insert(
            tk.END,
            f"- Lemak: {food['fat']} g\n"
        )
        self.trace.insert(
            tk.END,
            f"- Serat: {food['fiber']} g\n"
        )
        self.trace.insert(
            tk.END,
            f"- Vegetarian: "
            f"{'Ya' if food['vegetarian'] else 'Tidak'}\n"
        )
        self.trace.insert(
            tk.END,
            f"- Alergen: "
            f"{', '.join(food['allergens']) if food['allergens'] else '-'}\n\n"
        )

        self.trace.insert(
            tk.END,
            "FAKTA TURUNAN & RULE YANG TERPICU:\n"
        )

        for line in item["trace"]:
            self.trace.insert(
                tk.END,
                f"✓ {line}\n"
            )


def run_cli():
    """Versi terminal untuk environment tanpa display, misalnya Google Colab/Jupyter."""
    print("\n=== NUTRITION FOOD ADVISOR - FORWARD CHAINING ===")
    print("Masukkan data user.\n")

    print("Tujuan:")
    print("1. Menurunkan")
    print("2. Menaikkan")
    print("3. Menjaga")
    pilihan = input("Pilih [1-3]: ").strip()
    goal_map = {"1": "Menurunkan", "2": "Menaikkan", "3": "Menjaga"}
    goal = goal_map.get(pilihan)
    if goal is None:
        print("Pilihan tujuan tidak valid.")
        return

    vegetarian_user = input("Vegetarian? [y/n]: ").strip().lower() == "y"

    raw_cal = input("Batas kalori opsional (Enter jika tidak ada): ").strip()
    if raw_cal:
        try:
            max_calories = float(raw_cal)
            if max_calories <= 0:
                raise ValueError
        except ValueError:
            print("Batas kalori harus berupa angka positif.")
            return
    else:
        max_calories = None

    print("\nAlergi:")
    for i, allergy in enumerate(ALLERGIES, 1):
        print(f"{i}. {allergy}")
    raw_allergy = input("Pilih [1-{}]: ".format(len(ALLERGIES))).strip()
    try:
        allergy = ALLERGIES[int(raw_allergy) - 1]
    except (ValueError, IndexError):
        print("Pilihan alergi tidak valid.")
        return

    results = recommend(goal, vegetarian_user, max_calories, allergy)

    print("\n=== HASIL REKOMENDASI ===")
    if not results:
        print("Tidak ada makanan yang memenuhi semua rule.")
        print("Coba ubah batas kalori, tujuan, atau pilihan lainnya.")
        return

    for i, item in enumerate(results, 1):
        food = item["food"]
        trace = item["trace"]
        allergens = ", ".join(food["allergens"]) if food["allergens"] else "-"
        print(f"\n{i}. {food['name']}")
        print(f"   Energi      : {food['energy']} kcal")
        print(f"   Protein     : {food['protein']} g")
        print(f"   Lemak       : {food['fat']} g")
        print(f"   Serat       : {food['fiber']} g")
        print(f"   Vegetarian  : {'Ya' if food['vegetarian'] else 'Tidak'}")
        print(f"   Alergen     : {allergens}")
        print("   Trace Forward Chaining:")
        for line in trace:
            print(f"      ✓ {line}")


def run_gui():
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except tk.TclError:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()

