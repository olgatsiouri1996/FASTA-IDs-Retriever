import os
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_file, ncbi, pipe, field, progress_bar):

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
    # Choose input data source and field seperator
    if ncbi and not pipe:
        command = f"awk 'sub(/^>(lcl|gnl|ref|sp|tr|emb|dbj)\|/, \"\")' {infile} | cut -d ' ' -f{field} > {outfile}"
    elif pipe and not ncbi:
        command = f"awk 'sub(/^>/, \"\")' {infile} | cut -d '|' -f{field} > {outfile}"
    elif ncbi and pipe:
        command = f"awk 'sub(/^>(lcl|gnl|ref|sp|tr)\|/, \"\")' {infile} | cut -d '|' -f{field} > {outfile}"
    else:
        command = f"awk 'sub(/^>/, \"\")' {infile} | cut -d ' ' -f{field} > {outfile}"
    
    try:
        subprocess.run(["wsl", "bash", "-c", command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        progress_bar.stop()
        messagebox.showinfo("Success", f"Output file created at: {os.path.abspath(outfile)}")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        print(f"Error: {e}")
        
def start_thread():
    input_file = input_file_var.get()
    ncbi = ncbi_var.get()
    pipe = pipe_var.get()
    field = field_var.get()

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input FASTA file.")
        return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, ncbi, pipe, field, progress_bar))
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

# Checkbox for additional option
ncbi_var = tk.BooleanVar(value=False)
tk.Checkbutton(app, text="Remove ncbi prefix for local/general/refseq/uniprot/EMBL/DDBJ databases", variable=ncbi_var).grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Checkbox for additional option
pipe_var = tk.BooleanVar(value=False)
tk.Checkbutton(app, text="Pipe(\"|\") as FASTA identifier/FASTA description seperator", variable=pipe_var).grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Number of threads input
tk.Label(app, text="Field number:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
field_var = tk.StringVar(value="1")
tk.Entry(app, textvariable=field_var, width=10).grid(row=3, column=1, padx=10, pady=10, sticky="w")


# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=5, column=1, padx=10, pady=20)

app.mainloop()
