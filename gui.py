import threading
import gi
from gi.repository import Gtk, GLib
import peerPackage.peer as peer
import asyncio

class AppWindow(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Peer2Peer")
        self.server = peer.Peer(6000, 6001, 7000)
        vbox = Gtk.VBox(spacing=6)
        self.msgs = Gtk.ListBox()
        self.send = Gtk.Entry()
        send_button = Gtk.Button(label="SEND")
        send_button.connect("clicked", self.send_message)
        vbox.pack_start(self.msgs, True, True, 0)
        vbox.pack_start(self.send, False, False, 0)
        vbox.pack_start(send_button, False, False, 0)
        self.add(vbox)

        self.listener_thread = threading.Thread(target=self.process_listener, daemon=True)
        self.listener_thread.start()

        self.check_messages()

    def check_messages(self):
        if hasattr(self, "new_message"):
            label = Gtk.Label(label=self.new_message)
            self.msgs.add(label)
            self.msgs.show_all()
            del self.new_message
        GLib.timeout_add(500, self.check_messages)

    def process_listener(self):
        for message in self.server.listener():
            self.new_message = message
    def send_message(self, _widget):
        message = self.send.get_text().strip()
        if message:
            self.server.send(message)
            label = Gtk.Label(label=message)
            self.msgs.add(label)
            self.msgs.show_all()
            self.send.set_text("")
    def update_ui(self, data):
        label = Gtk.Label(label=data.decode())
        self.msgs.add(label)
        self.msgs.show_all()
        
win = AppWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

