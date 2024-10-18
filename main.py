from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog, messagebox
import tkinter

FORM_LBL_FONT = ('Arial', 12, "normal")


class ImageWatermarkApp:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Image Watermark App")
        self.window.config(padx=50, pady=50)

        canvas_my_app = tkinter.Canvas(width=300, height=200)
        tk_img_my_app = ImageTk.PhotoImage(Image.open('logo.jpg'))
        canvas_my_app.create_image(150, 100, image=tk_img_my_app)
        canvas_my_app.grid(row=0, column=1, pady=30)

        # Source image
        form_source_img_lbl = tkinter.Label(text='Image to be watermarked: ', font=FORM_LBL_FONT)
        form_source_img_lbl.grid(row=1, column=0)
        self.form_source_img_entry = tkinter.Entry(width=50)
        self.form_source_img_entry.grid(row=1, column=1)
        form_source_img_bt = tkinter.Button(text="Browse...", width=20,
                                            command=lambda: self.open_filedialog(
                                                destination_entry=self.form_source_img_entry),
                                            highlightthickness=0)
        form_source_img_bt.grid(row=1, column=3)

        # Watermark to be placed
        form_watermark_img_lbl = tkinter.Label(text='Watermark to be placed: ', font=FORM_LBL_FONT)
        form_watermark_img_lbl.grid(row=2, column=0)
        self.form_watermark_img_entry = tkinter.Entry(width=50)
        self.form_watermark_img_entry.grid(row=2, column=1)
        form_watermark_img_bt = tkinter.Button(text="Browse...", width=20,
                                               command=lambda: self.open_filedialog(
                                                   destination_entry=self.form_watermark_img_entry),
                                               highlightthickness=0)
        form_watermark_img_bt.grid(row=2, column=3)

        # Begin button
        begin_bt = tkinter.Button(text="Watermark image!", width=50, command=self.watermark_image)
        begin_bt.grid(row=3, column=1, pady=30)

        # Canvas result
        self.canvas_result = tkinter.Canvas(width=300, height=300)
        self.canvas_result.grid(row=4, column=0, columnspan=3)
        self.canvas_result.grid_remove()

        self.window.mainloop()

    @staticmethod
    def open_filedialog(destination_entry: tkinter.Entry):
        file_path = filedialog.askopenfilename(title='Select an image',
                                               filetypes=[('Images', '*.png;*.jpg;*.jpeg;*.gif')])
        if file_path:
            destination_entry.insert(0, file_path)

    @staticmethod
    def show_img(event, img: Image):
        img.show()

    def watermark_image(self):
        img_fpath = self.form_source_img_entry.get().strip()
        watermark_fpath = self.form_watermark_img_entry.get().strip()

        if not img_fpath or not watermark_fpath:
            messagebox.showerror(title='Oops', message='Please, input the path for both image and watermark image files.')
            return

        img = Image.open(img_fpath).convert('RGBA')
        watermark = Image.open(watermark_fpath).convert('RGBA')

        # Adjust watermark opacity
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(0.8)
        watermark.putalpha(alpha)

        watermark = watermark.rotate(30, expand=True)

        img_width, img_height = img.size
        watermark_width, watermark_height = watermark.size

        should_paste = True
        for i in range(0, img_width, watermark_width + 100):
            for j in range(0, img_height, watermark_height + 75):
                if should_paste:
                    img.paste(watermark, (i, j), watermark)
                    should_paste = False
                else:
                    should_paste = True

        img_copy = img.copy()
        img_copy.thumbnail((300, 300))
        tk_img = ImageTk.PhotoImage(img_copy)

        self.canvas_result.create_image(0, 0, anchor="nw", image=tk_img)
        self.canvas_result.grid()
        self.canvas_result.image = tk_img
        self.canvas_result.bind("<Button-1>", lambda event: self.show_img(event, img))

        # img.show()

        return None


        # destination_file = filedialog.asksaveasfilename(title='Save the new image as...',
        #                                                 defaultextension='.png',
        #                                                 filetypes=[('PNG File', '*.png')]
        #                                                 )
        # if destination_file:
        #     # TODO: finish watermarking process
        #     print(destination_file)



if __name__ == '__main__':
    app = ImageWatermarkApp()
