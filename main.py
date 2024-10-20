import time

from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog, messagebox
import tkinter, os

FORM_LBL_FONT = ('Arial', 12, "normal")


class ImageWatermarkApp:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Image Watermark App")
        self.window.config(padx=50, pady=50)
        self._current_row = 0

        self._preview_hidden = True

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

        # Watermark reduce size scale
        lbl_wk_size_reduction = tkinter.Label(text='Watermark reduce size in %:', font=FORM_LBL_FONT)
        lbl_wk_size_reduction.grid(row=3, column=0)
        self.scale_wk_size_reduction = tkinter.Scale(from_=0, to=100, orient=tkinter.HORIZONTAL, length=250,
                                                   command=self.on_scale_change)
        self.scale_wk_size_reduction.grid(row=3, column=1)

        # Watermark rotation scale
        lbl_wk_rotation = tkinter.Label(text='Watermark rotation angle: ', font=FORM_LBL_FONT)
        lbl_wk_rotation.grid(row=4, column=0)
        self.scale_wk_rotation = tkinter.Scale(from_=0, to=360, orient=tkinter.HORIZONTAL, length=250, command=self.on_scale_change)
        self.scale_wk_rotation.grid(row=4, column=1)

        # Watermark opacity scale
        lbl_wk_transparency = tkinter.Label(text='Watermark transparency:', font=FORM_LBL_FONT)
        lbl_wk_transparency.grid(row=5, column=0)
        self.scale_wk_transparency = tkinter.Scale(from_=0, to=100, orient=tkinter.HORIZONTAL, length=250, command=self.on_scale_change)
        self.scale_wk_transparency.grid(row=5, column=1)

        # Watermark Image button
        watermark_img_bt = tkinter.Button(text="Watermark image!", width=50, command=self.watermark_image)
        watermark_img_bt.grid(row=6, pady=30, sticky='ew', columnspan=6)

        # Canvas result
        self.canvas_result = tkinter.Canvas(width=600, height=300)
        self.canvas_result.grid(row=7, columnspan=6,  sticky='ew')
        self.canvas_result.grid_remove()

        # Save watermarked image button
        self.save_img_bt = tkinter.Button(text='Save watermarked image as...', width=50)
        self.save_img_bt.grid(row=8, columnspan=6, sticky='ew')
        self.save_img_bt.grid_remove()

        self.window.mainloop()

    @staticmethod
    def open_filedialog(destination_entry: tkinter.Entry):
        file_path = filedialog.askopenfilename(title='Select an image',
                                               filetypes=[('Images', '*.png;*.jpg;*.jpeg;*.gif')])
        if file_path:
            destination_entry.delete(0, 'end')
            destination_entry.insert(0, file_path)

    @staticmethod
    def show_img(event, img: Image):
        img.show()

    def on_scale_change(self, value):
        self.update_preview()

    def get_real_defined_transparency(self):
        return 1 - float(self.scale_wk_transparency.get() / 100)

    def reduce_img_size(self, current_size: tuple):
        cur_width, cur_height = current_size
        reduction_factor = 1 - float(self.scale_wk_size_reduction.get() / 100)
        return int(cur_width * reduction_factor), int(cur_height * reduction_factor)

    def update_preview(self):
        if hasattr(self.canvas_result, 'image') and self.canvas_result.image is not None:
            self.watermark_image()

    def watermark_image(self):
        img_fpath = self.form_source_img_entry.get().strip()
        watermark_fpath = self.form_watermark_img_entry.get().strip()

        if not img_fpath or not watermark_fpath:
            messagebox.showerror(title='Oops',
                                 message='Please, input the path for both image and watermark image files.')
            return

        img = Image.open(img_fpath).convert('RGBA')
        watermark = Image.open(watermark_fpath).convert('RGBA')

        # Adjust watermark size
        if self.scale_wk_size_reduction.get() != 0:
            watermark = watermark.resize(self.reduce_img_size(watermark.size))

        # Adjust watermark opacity
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.get_real_defined_transparency())
        watermark.putalpha(alpha)

        watermark = watermark.rotate(self.scale_wk_rotation.get(), expand=True)

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
        img_copy.thumbnail((600, 600))
        tk_img = ImageTk.PhotoImage(img_copy)

        self.canvas_result.create_image(0, 0, anchor="nw", image=tk_img)
        self.canvas_result.image = tk_img

        # Shows the save image button
        if self._preview_hidden:
            self.canvas_result.grid()
            self.save_img_bt.grid()
            self._preview_hidden = False

        self.canvas_result.bind("<Button-1>", lambda event: self.show_img(event, img))
        self.save_img_bt.config(command=lambda: self.save_watermarked_image(img))

    @staticmethod
    def save_watermarked_image(img: Image):
        destination_filepath = filedialog.asksaveasfilename(title='Save the new image as...',
                                                            defaultextension='.png',
                                                            filetypes=[('PNG File', '*.png')]
                                                            )
        if destination_filepath:
            img.save(destination_filepath, "png")
            question = messagebox.askyesno(title='Success', message='Image saved successfully!\nWould you like to open the destination folder?')
            if question:
                destination_folder = destination_filepath[:destination_filepath.rindex('/')]
                os.startfile(destination_folder)


if __name__ == '__main__':
    app = ImageWatermarkApp()
