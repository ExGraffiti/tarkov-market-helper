import wx
from mouse import get_position
from time import sleep
from threading import Thread
from pandas import DataFrame
from scan import Scan
from items import Items


class MainFrame(wx.Frame):
    def __init__(self, fps, API_KEY, screen_width, screen_height):
        """
        Init of MainFrame that show item price when mouse is pointing on an item

        Arguments:
        fps -- how often will be updated MainFrame
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Set style and options of Frame
        style = (wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.SIMPLE_BORDER)
        super().__init__(None, title='Tarkov Market Helper', size=(126, 82), style=style)
        self.panel = wx.Panel(self)
        self.SetTransparent(220)
        self.SetBackgroundColour('black')

        # Items init with chosen lang
        self.items = Items(API_KEY)

        # Remember prev item hash to compare with current item hash (for optimization)
        self.previous_item_hash = ''

        # Starting value for item values
        self.item = DataFrame()
        self.item_state = 'No item'

        # MainFrame update time with fps value that get from settings
        self.update_time = 1 / fps

        # Init UI
        self.min_price_text = None
        self.price_text = None
        self.slot_price_text = None
        self.trader_price_text = None
        self.init_ui()

        # Starting thread for positioning frame
        self.thread_is_on = True
        self.turn_thread()

    def turn_thread(self):
        """
        Changing thread bool and then start thread
        """
        self.thread_is_on = not self.thread_is_on

        if self.thread_is_on:
            thread = Thread(target=self.thread_frames)
            thread.start()

    def thread_frames(self):
        """
        Thread body that looping while is on
        """
        while self.thread_is_on:
            self.update_frame()
            sleep(self.update_time)

        self.Show(False)

    def update_frame(self):
        """
        Update frame with position, item hash and UI
        """
        # Update mouse position
        pos_x, pos_y = get_position()
        wx.CallAfter(self.Move, wx.Point(pos_x + 10, pos_y + 20))

        # Scan item that set item_hash and item_state
        self.scan_item()

        # Update item info in UI
        if self.item and self.item_state == True:

            self.update_ui()

        elif not self.item and self.item_state == "Item data not found" \
                and self.previous_item_hash != "":
            self.previous_item_hash = ""
            self.update_ui()

    def init_ui(self):
        """
        Init UI when app start
        """
        hbox = wx.BoxSizer()
        fb = wx.FlexGridSizer(4, 2, 1, 4)

        min_price_title = wx.StaticText(self.panel, size=(12, 16), label='N:', style=wx.ALIGN_CENTRE_HORIZONTAL)
        min_price_title.SetForegroundColour((160, 160, 170))

        self.min_price_text = wx.StaticText(self.panel, label=f'None')
        self.min_price_text.SetForegroundColour((240, 226, 42))

        price_title = wx.StaticText(self.panel, size=(12, 16), label='P:', style=wx.ALIGN_CENTRE_HORIZONTAL)
        price_title.SetForegroundColour((160, 160, 170))

        self.price_text = wx.StaticText(self.panel, label=f'N/A')
        self.price_text.SetForegroundColour((240, 226, 42))

        slot_price_title = wx.StaticText(self.panel, size=(12, 16), label='S:', style=wx.ALIGN_CENTRE_HORIZONTAL)
        slot_price_title.SetForegroundColour((160, 160, 170))

        self.slot_price_text = wx.StaticText(self.panel, label=f'N/A')
        self.slot_price_text.SetForegroundColour((240, 226, 42))

        trader_price_title_ = wx.StaticText(self.panel, size=(12, 16), label='T:', style=wx.ALIGN_CENTRE_HORIZONTAL)
        trader_price_title_.SetForegroundColour((160, 160, 170))

        self.trader_price_text = wx.StaticText(self.panel, label=f'N/A')
        self.trader_price_text.SetForegroundColour((240, 226, 42))

        fb.AddMany([min_price_title, self.min_price_text,
                    price_title, self.price_text,
                    slot_price_title, self.slot_price_text,
                    trader_price_title_, self.trader_price_text,
                    ])

        hbox.Add(fb, proportion=1, flag=wx.EXPAND | wx.ALL, border=6)
        self.panel.SetSizer(hbox)
        self.Layout()

    def update_ui(self):
        """
        Update UI when thread looping
        """
        if self.item_state == True:
            self.min_price_text.SetLabel(f"{self.item['name']}")
            self.price_text.SetLabel(f"₽{self.item['avg']}")
            self.slot_price_text.SetLabel(f"₽{self.item['avg_per_slot']}")
            self.trader_price_text.SetLabel(f"₽{self.item['trader']}")

        elif self.item_state == False:
            self.min_price_text.SetLabel('None')
            self.price_text.SetLabel('N/A')
            self.slot_price_text.SetLabel('N/A')
            self.trader_price_text.SetLabel('N/A')

    def scan_item(self):
        """
        Scan item when thread looping and set item_hash, item_state
        """
        try:
            self.item, self.item_state, show = self.items.find(Scan(self.screen_width, self.screen_height).item_hash)

        except AttributeError as error:
            print(error)
            self.item, self.item_state = self.items.find('')
            show = False

        if self.item and self.item_state == True and show == True:
            self.Show(True)

        elif self.item and self.item_state == False and show == True:
            self.Show(True)

        else:
            self.Show(False)

    def note_item(self):
        """
        Used for debug purpose
        """
        # print(f'Debug Hash: {self.item_state}: {Scan().item_hash}')
        ...
