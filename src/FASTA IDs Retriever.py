import os
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_file, progress_bar):

    # Start the progress bar
    progress_bar.start()

    # Select input directory
    input_directory = os.path.dirname(input_file)

    # Select input file
    infile = os.path.basename(input_file)
    
    # Select output file
    outfile = f"{os.path.splitext(infile)[0]}_ids.txt"

    # Change to the input file's directory
    os.chdir(input_directory)

    # Run command
    command = f"awk 'sub(/^>/, \"\")' {infile} | cut -d ' ' -f1 > {outfile}"
    
    try:
        subprocess.run(["wsl", "bash", "-c", command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        progress_bar.stop()
        messagebox.showinfo("Success", f"Output file created at: {os.path.abspath(outfile)}")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        print(f"Error: {e}")
        
def start_thread():
    input_file = input_file_var.get()
    
    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input FASTA file.")
        return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, progress_bar))
    thread.start()

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("FASTA IDs Retriever")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input FASTA File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=1, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=2, column=1, padx=10, pady=20)

app.mainloop()
