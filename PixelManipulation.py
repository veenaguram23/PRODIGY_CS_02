import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Encryption logic
def encrypt_decrypt_image(img, key, mode='encrypt'):
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if mode == 'encrypt':
                r = (r + key) % 256
                g = (g + key) % 256
                b = (b + key) % 256
            else:
                r = (r - key) % 256
                g = (g - key) % 256
                b = (b - key) % 256
            pixels[x, y] = (r, g, b)
    return img

#Validatation key logic 
def validate_key(key):
    if key <= 0:
        messagebox.showwarning("Invalid Key", "Please enter a positive integer key.")
        return False
    return True

#Image opening Logic
def open_image():
    global img, img_display
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        img = Image.open(file_path)
        display_image(img)
        img_info.set(f"Format: {img.format} | Size: {img.size[0]} x {img.size[1]} px")
        btn_encrypt.config(state='normal')
        btn_decrypt.config(state='normal')

#Image Displaying Logic 
def display_image(image):
    global img_display
    img_resized = image.copy()
    img_resized.thumbnail((350, 350))
    img_display = ImageTk.PhotoImage(img_resized)
    label_img.config(image=img_display)
    label_img.image = img_display

#Image Processing Logic 
def process_image(mode):
    global img
    try:
        key = int(entry_key.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Key must be an integer.")
        return
    if not validate_key(key):
        return
    if img is None:
        messagebox.showwarning("No Image", "Please open an image first.")
        return

    processed = encrypt_decrypt_image(img.copy(), key, mode)
    display_image(processed)

    save_path = filedialog.asksaveasfilename(
        title="Save Image As",
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("Bitmap", "*.bmp")]
    )
    if save_path:
        processed.save(save_path)
        messagebox.showinfo("Success", f"Image saved to:\n{save_path}")

#Reseting the window 
def reset_all():
    global img, img_display
    img = None
    img_display = None
    label_img.config(image='')
    img_info.set("")
    entry_key.delete(0, tk.END)
    btn_encrypt.config(state='disabled')
    btn_decrypt.config(state='disabled')

# Main window setup
root = tk.Tk()
root.title("Image Encryption Tool")
root.minsize(600, 600)  # Minimum size to prevent too small a window
root.resizable(True, True)  # Allow window resizing (minimize/maximize)
root.config(bg="#f5f7fa")


# Style setup for ttk buttons
style = ttk.Style(root)
style.configure('TButton', font=('Segoe UI', 11), padding=6)
style.map('TButton', background=[('active', '#4a90e2')], foreground=[('active', 'white')])

# Title Frame
frame_title = tk.Frame(root, bg="#f5f7fa", pady=15)
frame_title.pack()
title_label = tk.Label(frame_title, text="Simple Image Encryption Tool", font=("Segoe UI", 18, "bold"), bg="#f5f7fa", fg="#333")
title_label.pack()

# Instructions
instructions = tk.Label(root, text="Open an image, enter a key (1-255), then encrypt or decrypt.",
                        font=("Segoe UI", 10), bg="#f5f7fa", fg="#555")
instructions.pack(pady=(0,15))

# Controls Frame
frame_controls = tk.Frame(root, bg="#f5f7fa")
frame_controls.pack(pady=10, padx=10, fill='x')

btn_open = ttk.Button(frame_controls, text="Open Image", command=open_image)
btn_open.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

tk.Label(frame_controls, text="Key:", font=("Segoe UI", 11), bg="#f5f7fa").grid(row=0, column=1, padx=5)
entry_key = ttk.Entry(frame_controls, width=8, font=("Segoe UI", 11))
entry_key.grid(row=0, column=2, padx=5)

btn_encrypt = ttk.Button(frame_controls, text="Encrypt", command=lambda: process_image('encrypt'), state='disabled')
btn_encrypt.grid(row=0, column=3, padx=5)

btn_decrypt = ttk.Button(frame_controls, text="Decrypt", command=lambda: process_image('decrypt'), state='disabled')
btn_decrypt.grid(row=0, column=4, padx=5)

btn_reset = ttk.Button(frame_controls, text="Reset", command=reset_all)
btn_reset.grid(row=0, column=5, padx=5)

for i in range(6):
    frame_controls.grid_columnconfigure(i, weight=1)

# Image display frame
frame_image = tk.Frame(root, bg="white", bd=2, relief="sunken")
frame_image.pack(pady=15, padx=20, fill='both', expand=True)

label_img = tk.Label(frame_image, bg="white")
label_img.pack(expand=True)

img_info = tk.StringVar()
label_info = tk.Label(root, textvariable=img_info, font=("Segoe UI", 10), bg="#f5f7fa", fg="#666")
label_info.pack(pady=5)

root.mainloop()
