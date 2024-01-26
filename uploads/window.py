import hexchat
import gi
gi.require_version("Gtk", "2.0")
from gi.repository import Gtk

__module_name__ = "Channel Modes"
__module_version__ = "1.0"
__module_description__ = "GTK window with buttons to set modes on the current HexChat channel"

class ModesWindow(Gtk.Window):
    def __init__(self):
        super(ModesWindow, self).__init__(title="Channel Modes")
        self.set_border_width(10)
        self.set_default_size(200, 100)

        vbox = Gtk.VBox(homogeneous=False, spacing=6)
        self.add(vbox)

        button1 = Gtk.Button(label="Set Mode +m")
        button1.connect("clicked", self.on_mode_m_clicked)
        vbox.pack_start(button1, True, True, 0)

        button2 = Gtk.Button(label="Set Mode +i")
        button2.connect("clicked", self.on_mode_i_clicked)
        vbox.pack_start(button2, True, True, 0)

        button3 = Gtk.Button(label="Set Mode +s")
        button3.connect("clicked", self.on_mode_s_clicked)
        vbox.pack_start(button3, True, True, 0)

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, True, True, 0)

        button4 = Gtk.Button(label="Check Ban Impact")
        button4.connect("clicked", self.on_check_ban_clicked)
        vbox.pack_start(button4, True, True, 0)

    def on_mode_m_clicked(self, button):
        hexchat.command("mode +m")

    def on_mode_i_clicked(self, button):
        hexchat.command("mode +i")

    def on_mode_s_clicked(self, button):
        hexchat.command("mode +s")

    def on_check_ban_clicked(self, button):
        ban_mask = self.entry.get_text()
        users = hexchat.get_list("users")
        if users is None:
            print("No users in the current channel.")
            return

        matching_users = [user for user in users if self.matches_ban_mask(user.nick, ban_mask)]
        percentage = len(matching_users) / len(users) * 100
        print(f"The ban would affect {percentage}% of the channel.")

    @staticmethod
    def matches_ban_mask(nick, ban_mask):
        # This is a simple implementation that only checks if the nick is in the ban mask.
        # You might want to replace this with a more sophisticated matching algorithm.
        return nick in ban_mask

# Rest of the code...