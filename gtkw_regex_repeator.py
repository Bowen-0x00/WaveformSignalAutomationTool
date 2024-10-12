import tkinter as tk
from tkinter import filedialog
import re

def replace_first_group(s, p, v):
    def replacement(match):
        full_match = match.group(0)
        first_group = match.group(1)
        return full_match.replace(first_group, v, 1)
    result = re.sub(p, replacement, s)
    return result

class GTKWaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("GTKWave Signal Editor")
        self.file_path = tk.StringVar()
        self.regex_pattern = tk.StringVar()
        self.duplicate_count = tk.IntVar(value=1)
        self.matched_signals = tk.StringVar()
        self.preview_signals = tk.StringVar()

        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="GTKW File:").grid(row=0, column=0, sticky='e')
        tk.Entry(self.root, textvariable=self.file_path, width=50).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.load_file).grid(row=0, column=2)
        tk.Label(self.root, text="Regex Pattern:").grid(row=1, column=0, sticky='e')
        regex_entry = tk.Entry(self.root, textvariable=self.regex_pattern, width=50)
        regex_entry.grid(row=1, column=1)
        regex_entry.bind('<KeyRelease>', self.update_matched_signals)
        tk.Label(self.root, text="Duplicate Count:").grid(row=2, column=0, sticky='e')
        duplicate_entry = tk.Entry(self.root, textvariable=self.duplicate_count, width=10)
        duplicate_entry.grid(row=2, column=1, sticky='w')
        duplicate_entry.bind('<KeyRelease>', self.update_preview)
        tk.Label(self.root, text="Matched Signals:").grid(row=3, column=0, sticky='ne')
        self.matched_signals_text = tk.Text(self.root, height=10, width=70, wrap='word', state='disabled')
        self.matched_signals_text.grid(row=3, column=1, columnspan=2, sticky='w')
        tk.Label(self.root, text="Preview Duplicated Signals:").grid(row=4, column=0, sticky='ne')
        self.preview_signals_text = tk.Text(self.root, height=10, width=70, wrap='word', state='disabled')
        self.preview_signals_text.grid(row=4, column=1, columnspan=2, sticky='w')
        tk.Button(self.root, text="Process and Save", command=self.process_file).grid(row=5, column=1, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("GTKWave Files", "*.gtkw")])
        if file_path:
            self.file_path.set(file_path)
            self.file_lines = open(file_path, 'r').readlines()
            self.update_matched_signals()

    def update_matched_signals(self, event=None):
        file_path = self.file_path.get()
        pattern = self.regex_pattern.get()
        if not file_path or not pattern:
            return
        try:
            lines = self.file_lines
            matched_signals = []
            begin = len(lines)
            end = 0
            for i, line in enumerate(lines):
                if len(line) >= 1 and line[0] in ["[", "@", "-"]:
                    continue
                match = re.match(pattern, line)
                if match:
                    signal = {}
                    signal['pre'] = lines[i-1].strip() if i > 0 and lines[i-1].startswith('@') else ''
                    signal['sig'] = line.strip()
                    signal['index'] = int(match.group(1))
                    matched_signals.append(signal)

                    begin = i if i < begin else begin
                    end = i if i > end else end

            self.matched_signals_text.config(state='normal')
            self.matched_signals_text.delete(1.0, tk.END)
            self.matched_signals_text.insert(tk.END, "\n".join(map(lambda x: x['sig'], matched_signals)))
            self.matched_signals_text.config(state='disabled')

            duplicate_count = self.duplicate_count.get()
            preview_text = ''

            for i in range(duplicate_count):
                preview_text += f'-{i}\n'
                for signal in matched_signals:
                    modified_signal = replace_first_group(signal['sig'], pattern, str(signal['index'] + i))
                    preview_text += signal['pre'] + '\n'
                    preview_text += modified_signal + '\n'
                preview_text += f'-{i}\n'
            self.preview_duplicated_signals(preview_text)
            self.content = '\n'.join(lines[:begin]) + preview_text + '\n'.join(lines[end+1:]) 

        except Exception as e:
            print(e)


    def update_preview(self, event=None):
        self.update_matched_signals()

    def preview_duplicated_signals(self, preview_text):
        self.preview_signals_text.config(state='normal')
        self.preview_signals_text.delete(1.0, tk.END)
        self.preview_signals_text.insert(tk.END, preview_text)
        self.preview_signals_text.config(state='disabled')

    def process_file(self):
        with open(self.file_path.get(), 'w') as f:
            f.write(self.content)

if __name__ == "__main__":
    root = tk.Tk()
    app = GTKWaveEditor(root)
    root.mainloop()
