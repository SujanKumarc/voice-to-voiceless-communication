import tkinter as tk

def test_image_loading():
    root = tk.Tk()
    try:
        img = tk.PhotoImage(file="hot_drink.png")
        label = tk.Label(root, image=img)
        label.pack()
        root.mainloop()
    except Exception as e:
        print(f"Error loading image: {e}")

if __name__ == "__main__":
    test_image_loading()
