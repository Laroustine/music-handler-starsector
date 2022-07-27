import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")
        self.loc_cbm = ""
        self.loc_result = ""
        self.title_bar()
        self.ui()

    def title_bar(self):    
        self.set_icon_from_file("assets/icon.png")
        self.set_title("Starsector Music Handler")
        self.set_default_size(400, 300)
        self.set_border_width(15)
        self.connect("destroy", Gtk.main_quit)
        self.grid = Gtk.Grid()
        self.add(self.grid)

    def ui(self):
        btn1 = Gtk.Button(label="Quit1")
        btn2 = Gtk.Button(label="Quit2")
        btn3 = Gtk.Button(label="Quit3")
        btn4 = Gtk.Button(label="Quit4")
        btn5 = Gtk.Button(label="Quit5")
        
        btn1.connect("clicked", self.on_folder_clicked)

        self.grid.attach(btn1, 0, 0, 1, 1)
        self.grid.attach(btn2, 2, 2, 1, 1)

    def on_button_clicked(self, widget):
        print("Hello World")
        
    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select Reseult Location",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
        dialog.destroy()


win = MyWindow()
win.show_all()
Gtk.main()
