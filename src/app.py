import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

from pipeline.match_pipeline import run_match




class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("brink - V1")
        self.geometry("780x480")

        # Top controls
        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.demo_var = tk.StringVar(value="")
        tk.Entry(top, textvariable=self.demo_var).pack(side="left", fill="x", expand=True)

        tk.Button(top, text="Select .dem", command=self.pick_demo).pack(side="left", padx=6)
        tk.Button(top, text="Run", command=self.run_clicked).pack(side="left")

        # Status line
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self, textvariable=self.status_var, anchor="w").pack(fill="x", padx=10)

        # Table
        cols = ("player", "kills", "deaths", "assists")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180 if c == "player" else 120, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Metadata
        self.meta_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.meta_var, anchor="w").pack(fill="x", padx=10, pady=(0, 10))

    def pick_demo(self):
        path = filedialog.askopenfilename(
            title="Select a CS2 .dem file",
            filetypes=[("CS2 demo files", "*.dem"), ("All files", "*.*")]
        )
        if path:
            self.demo_var.set(path)

    def run_clicked(self):
        demo_path = self.demo_var.get().strip()
        if not demo_path:
            messagebox.showwarning("Missing demo", "Select a .dem file first.")
            return

        self.status_var.set("Running pipeline… (parsing demo)")
        self.meta_var.set("")
        self.clear_table()

        # Run pipeline in a thread so the UI doesn't freeze
        t = threading.Thread(target=self._run_pipeline_thread, args=(demo_path,), daemon=True)
        t.start()

    def _run_pipeline_thread(self, demo_path: str):
        try:
            result = run_match(demo_path)

            rows = result["rows"]
            match_id = result["match_id"]
            map_name = result["map_name"]
            parsed_folder = result["parsed_folder"]

            self.after(0, lambda: self.populate(rows, match_id, map_name, parsed_folder))
        except Exception as e:
            msg = str(e)
            self.after(0, lambda: self.status_var.set("Failed."))
            self.after(0, lambda m=msg: messagebox.showerror("Error", m))



    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def populate(self, rows, match_id, map_name, parsed_folder):
        for r in rows:
            self.tree.insert("", "end", values=(r["player"], r["kills"], r["deaths"], r["assists"]))

        self.status_var.set("Done. (DB insert attempted; GUI always shows results.)")
        self.meta_var.set(f"match_id: {match_id} | map: {map_name} | output: {parsed_folder}")


if __name__ == "__main__":
    App().mainloop()
