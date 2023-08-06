#!/usr/bin/env python
import gi
gi.require_version('GSound', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk, GLib, Gdk, GSound, Pango, PangoCairo, GdkPixbuf
__import__("glib")
import re
import yaml
import os
from typing import List, Dict

from . import dbus

def PANGO_PIXELS_CEIL(d):
    return (int(d) + 1023) >> 10

def parse_colour(s):
    m = re.match(r'([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})', s)
    if m:
        return [int(m.group(i), 16) / 256 for i in range(1, 4)]
    else:
        raise Exception("Invalid colour {}".format(s))

def make_popup(configuration, text="", icon_name=None, progress=None):
    win = Gtk.Window(type="popup")

    area = Gtk.DrawingArea()
    win.add(area)

    context = win.create_pango_context()
    desc = context.get_font_description()
    desc.set_family(configuration['font-family'])
    desc.set_size(configuration['font-size'] * Pango.SCALE)
    context.set_font_description(desc)

    hints = Gdk.Geometry()
    hints.max_width = 400
    hints.max_height = 500

    layout = Pango.Layout(context)
    layout.set_width(hints.max_width * Pango.SCALE)
    layout.set_markup(text, len(text))

    theme = Gtk.IconTheme.get_default()
    icon_size = configuration['icon-size']
    margin = configuration['margin']

    text_rect = Gdk.Rectangle()
    icon_rect = Gdk.Rectangle()
    frame_rect = Gdk.Rectangle()

    text_rect.x = margin
    text_rect.y = margin
    icon_rect.x = margin
    icon_rect.y = margin

    if progress is None:
        ink, logical = layout.get_extents()
        text_rect.width = PANGO_PIXELS_CEIL(logical.width)
        text_rect.height = PANGO_PIXELS_CEIL(logical.height)
    else:
        text_rect.width = configuration['progress-width']
        text_rect.height = configuration['progress-height']

    if icon_name is None:
        icon = None
        icon_rect.width = 0
        icon_rect.height = 0
        total_height = text_rect.height
    else:
        if os.path.exists(icon_name):
            icon = GdkPixbuf.Pixbuf.new_from_file(icon_name)
        else:
            icon = theme.load_icon(icon_name, icon_size, 0)

        icon_rect.width = icon.get_width()
        icon_rect.height = icon.get_height()

        text_rect.x += margin + icon_rect.width

        total_height = max(text_rect.height, icon_rect.height)
        text_rect.y += (total_height - text_rect.height) // 2;
        icon_rect.y += (total_height - icon_rect.height) // 2;

    frame_rect.x = 0
    frame_rect.y = 0
    frame_rect.width = text_rect.x + text_rect.width + margin
    frame_rect.height = total_height + margin * 2

    win.set_default_size(frame_rect.width, frame_rect.height)
    # win.set_geometry_hints(None, hints, Gdk.WindowHints.MAX_SIZE)

    popup = Popup(configuration=configuration,
                  win=win,
                  rect=frame_rect,
                  text_rect=text_rect,
                  icon_rect=icon_rect,
                  layout=layout,
                  icon=icon,
                  progress=progress)
    area.connect("draw", popup.draw)
    return popup

class Popup(object):
    def __init__(self, configuration, win, rect, text_rect,
                 icon_rect, layout, icon, progress):
        self.configuration = configuration
        self.win = win
        self.rect = rect
        self.text_rect = text_rect
        self.icon_rect = icon_rect
        self.layout = layout
        self.icon = icon
        self.progress = progress

    def draw(self, widget, cr):
        bg = self.configuration['background']
        cr.set_source_rgb(bg[0], bg[1], bg[2])
        cr.paint()

        if self.icon:
            cr.save()
            cr.translate(self.icon_rect.x,
                         self.icon_rect.y)
            Gdk.cairo_set_source_pixbuf(cr, self.icon, 0, 0)
            cr.paint()
            cr.restore()

        cr.save()
        cr.translate(self.text_rect.x,
                     self.text_rect.y)
        if self.progress is None:
            fg = self.configuration['text']
            cr.set_source_rgb(fg[0], fg[1], fg[2])
            PangoCairo.update_layout(cr, self.layout)
            PangoCairo.show_layout(cr, self.layout)
        else:
            fg = self.configuration['progress']
            cr.set_source_rgb(fg[0], fg[1], fg[2])
            w = int(self.text_rect.width / 100 * self.progress)
            cr.rectangle(0, 0, w, self.text_rect.height)
            cr.fill()
        cr.restore()
        return False

    def __del__(self):
        del self.win
        del self.layout
        del self.rect
        del self.text_rect
        del self.icon_rect
        del self.icon

def relative_offset(offset, size, total):
    if offset >= 0:
        return offset
    else:
        return total - size + offset

class IdSet(object):
    def __init__(self):
        self.next_id = 1
        self.reserved = set()

    def get(self, requested=0):
        if requested == 0:
            while self.next_id in self.reserved:
                self.reserved.remove(self.next_id)
                self.next_id += 1
            id = self.next_id
            self.next_id += 1
            return id
        else:
            if requested >= self.next_id:
                self.reserved.add(requested)
            return requested

class Display(object):
    def __init__(self, configuration, gsound_context):
        self.popups = []
        self.base_offsetx = configuration['base-x']
        self.base_offsety = configuration['base-y']
        self.offsety = configuration['offset']
        self.display = Gdk.Display.get_default()
        self.id_set = IdSet()
        self.configuration = configuration
        self.gsound_context = gsound_context

    def get_offsety(self, popup):
        y = self.base_offsety
        for p in self.popups:
            if p == popup: break
            if self.offsety > 0:
                y += self.offsety + p.rect.height
            else:
                y += self.offsety - p.rect.height
        return y

    def add(self, **args):
        sound_name = args['hints'].get('sound-name')
        if sound_name:
            self.gsound_context.play_simple(
                { GSound.ATTR_EVENT_ID: sound_name,
                  GSound.ATTR_EVENT_DESCRIPTION: "notification" })

        popup_id = self.id_set.get(args['replaces_id'])
        if not (args['summary'] or \
                args['body'] or \
                args['app_icon']):
            # empty message, do not display anything
            return popup_id

        msg = {}
        m = re.match(r'([0-9]+) %$', args['body'])
        if m:
            msg['progress'] = int(m.group(1))

        msg['text'] = "\n".join(line \
            for line in ["<b>{}</b>".format(args['summary']),
                        args['body']] \
            if line)
        if args['app_icon']:
            msg['icon_name'] = args['app_icon']

        popup = make_popup(self.configuration, **msg)
        popup.id = popup_id
        popup_idx = self.find_popup_index(popup_id)
        if popup_idx is None:
            self.popups.append(popup)
        else:
            old_popup = self.popups[popup_idx]
            self.popups[popup_idx] = popup
            old_popup.win.close()

        # realize top-level widget here to make sure that we can access its
        # underlying Gdk.Window
        popup.win.realize()
        self.update_all()

        if args['expire_timeout'] != -1:
            timeout = args['expire_timeout']
        else:
            timeout = self.configuration['timeout']
        timeout = max(timeout, self.configuration['min-timeout'])
        GLib.timeout_add(timeout, lambda: self.remove(popup))
        popup.win.show_all()

        return popup.id

    def kill(self, id):
        if id > 0:
            idx = self.find_popup_index(id)
        else:
            idx = -1
        if idx is not None:
            self.remove(self.popups[idx])

    def update(self, popup):
        monitor = self.display.get_monitor_at_window(popup.win.get_window())
        monitor_rect = monitor.get_geometry()
        y = self.get_offsety(popup)
        popup.win.move(
            relative_offset(self.base_offsetx,
                            popup.rect.width,
                            monitor_rect.x + monitor_rect.width),
            relative_offset(y,
                            popup.rect.height,
                            monitor_rect.y + monitor_rect.height))

    def update_all(self):
        for popup in self.popups:
            self.update(popup)

    def remove(self, popup):
        if popup in self.popups:
            self.popups.remove(popup)
            popup.win.close()
            del popup
            self.update_all()

    def find_popup_index(self, id):
        for i, p in enumerate(self.popups):
            if p.id == id:
                return i

@dbus.interface("org.freedesktop.Notifications")
class Notifications(object):
    def __init__(self, notify, kill):
        self._notify = notify
        self._kill = kill

    @dbus.export
    def GetServerInformation(self) -> [('name', str),
                                       ('vendor', str),
                                       ('version', str),
                                       ('spec_version', str)] :
        return ("osdd", "https://gitlab.com/pcapriotti/osd", "0.6", "1")

    @dbus.export
    def Notify(self,
               app_name : str,
               replaces_id : dbus.uint,
               app_icon : str,
               summary : str,
               body : str,
               actions : List[str],
               hints : Dict[str, dbus.variant],
               expire_timeout : int) -> ("response", dbus.uint) :
        return self._notify(app_name=app_name,
                            replaces_id=replaces_id,
                            app_icon=app_icon,
                            summary=summary,
                            body=body,
                            actions=actions,
                            hints=hints,
                            expire_timeout=expire_timeout)

    @dbus.export
    def Kill(self, id: int):
        return self._kill(id)

def get_configuration():
    conf = {
        'icon-size' : 24,
        'margin' : 5,
        'base-x' : -10,
        'base-y' : 10,
        'offset' : 10,
        'background' : (0.2, 0.2, 0.2),
        'text' : (1, 1, 1),
        'progress' : (1, 1, 1),
        'progress-width' : 300,
        'progress-height' : 25,
        'timeout': 5000,
        'min-timeout': 1000,
        'font-family': "sans",
        'font-size': 10
    }
    try:
        with open("{}/.config/osd/config.yaml".format(os.environ["HOME"])) as f:
            c = yaml.safe_load(f)
            for name in ['background', 'text', 'progress']:
                if name in c: c[name] = parse_colour(c[name])
            conf.update(c)
    except FileNotFoundError:
        pass
    return conf

def run():
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    gsound_context = GSound.Context()
    gsound_context.init()

    configuration = get_configuration()
    display = Display(configuration, gsound_context)

    dbus.publish_object("org.freedesktop.Notifications",
                        "/org/freedesktop/Notifications",
                        Notifications(display.add, display.kill))

    Gtk.main()
