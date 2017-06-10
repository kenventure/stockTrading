"""

This demo demonstrates how to embed a matplotlib (mpl) plot 

into a wxPython GUI application, including:



* Using the navigation toolbar

* Adding data to the plot

* Dynamically modifying the plot's properties

* Processing mpl events

* Saving the plot to a file from a menu



The main goal is to serve as a basis for developing rich wx GUI

applications featuring mpl plots (using the mpl OO API).



Eli Bendersky (eliben@gmail.com)

License: this code is in the public domain

Last modified: 30.07.2008

"""

import os

import pprint

import random

import wx

from TradeBroker import TradeBroker
from RSIAlgorithm import RSIAlgorithm
from Algorithm import Algorithm
import csv

# The recommended way to use wx with mpl is with the WXAgg

# backend. 

#

import matplotlib

matplotlib.use('WXAgg')

from matplotlib.figure import Figure

from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

from GUITradeBroker import GUITradeBroker




class MatPlotWxDisplay(wx.Frame):

    """ The main frame of the application

    """

    title = 'Demo: wxPython with matplotlib'

    

    def __init__(self):

        wx.Frame.__init__(self, None, -1, self.title)
        #self.data = [50]

        

        self.create_menu()

        self.create_status_bar()

        self.create_main_panel()

        

        self.RSITextbox.SetValue('50')

        self.draw_figure()
        self.readData()

        
    def readData(self):
        default_path='C:\\Users\\ktcm2\\Documents\\python\\stockTrading\\stockTrade(OO)'
        os.chdir(default_path)


        self.data=[]

        with open('EURCHF_m5_Bid.csv', 'rt') as f:
            reader = csv.reader(f)
            next(reader)
            for date, time, Open, high, low, close, tTicks in reader:
                tempRow={}
                tempRow['Date']=date
                tempRow['Time']=time
                tempRow['Open']=Open
                tempRow['High']=high
                tempRow['Low']=low
                tempRow['Close']=close
                tempRow['Ticks']=tTicks
                self.data.append(tempRow)    
        #self.rsiAlgorithm=RSIAlgorithm(intervalMin=5)
        #self.broker = GUITradeBroker(data = self.data, totalMoney=11000, invest=10000, algorithm = self.rsiAlgorithm)
        
    def create_menu(self):

        self.menubar = wx.MenuBar()

        

        menu_file = wx.Menu()

        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")

        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)

        menu_file.AppendSeparator()

        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")

        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)

        

        menu_help = wx.Menu()

        m_about = menu_help.Append(-1, "&About\tF1", "About the demo")

        self.Bind(wx.EVT_MENU, self.on_about, m_about)

        

        self.menubar.Append(menu_file, "&File")

        self.menubar.Append(menu_help, "&Help")

        self.SetMenuBar(self.menubar)



    def create_main_panel(self):

        """ Creates the main panel with all the controls on it:

             * mpl canvas 

             * mpl navigation toolbar

             * Control panel for interaction

        """

        self.panel = wx.Panel(self)

        

        # Create the mpl Figure and FigCanvas objects. 

        # 5x4 inches, 100 dots-per-inch

        #

        self.dpi = 100

        self.fig = Figure((5.0, 4.0), dpi=self.dpi)

        
        left, width = 0.1, 0.8
        rect1 = [left, 0.75, width, 0.2]
        rect2 = [left, 0.5, width, 0.2]
        rect3 = [left, 0.25, width, 0.2]
        rect4 = [left, 0.1, width, 0.1]
        #rect5 = [left, 0.1, width, 0.1]    
        textsize = 9        
        axescolor = '#f6f6f6'  # the axes background color
        self.ax1 = self.fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height
        self.ax1.text(0.025, 0.95, 'Equity', va='top', transform=self.ax1.transAxes, fontsize=textsize)
        
        self.ax2 = self.fig.add_axes(rect2, axisbg=axescolor)  # left, bottom, width, height
        self.ax2.text(0.025, 0.95, 'Price', va='top', transform=self.ax2.transAxes, fontsize=textsize)
        
        self.ax3 = self.fig.add_axes(rect3, axisbg=axescolor)  # left, bottom, width, height
        self.ax3.text(0.025, 0.95, 'RSI', va='top', transform=self.ax3.transAxes, fontsize=textsize)
        
        self.ax4 = self.fig.add_axes(rect4, axisbg=axescolor)  # left, bottom, width, height
        self.ax4.text(0.025, 0.95, 'Buy / Sell', va='top', transform=self.ax4.transAxes, fontsize=textsize)
        
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        #self.ax5 = self.fig.add_axes(rect5, axisbg=axescolor)  # left, bottom, width, height
        #self.ax5.text(0.025, 0.95, 'Sell', va='top', transform=self.ax5.transAxes, fontsize=textsize)
        # Since we have only one plot, we can use add_axes 

        # instead of add_subplot, but then the subplot

        # configuration tool in the navigation toolbar wouldn't

        # work.

        #

        #self.axes = self.fig.add_subplot(111)

        

        # Bind the 'pick' event for clicking on one of the bars

        #

        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.RSIStaticTxt = wx.StaticText(self.panel,-1,style = wx.ALIGN_CENTER) 
		

		
        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        self.RSIStaticTxt.SetFont(font) 
        self.RSIStaticTxt.SetLabel('RSI Buy Value') 
       

        self.RSITextbox = wx.TextCtrl(

            self.panel, 

            size=(200,-1),

            style=wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.RSITextbox)

        

        self.tradebutton = wx.Button(self.panel, -1, "Start Trading")

        self.Bind(wx.EVT_BUTTON, self.on_trade_button, self.tradebutton)



        self.cb_grid = wx.CheckBox(self.panel, -1, 

            "Show Grid",

            style=wx.ALIGN_RIGHT)

        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)



        self.slider_label = wx.StaticText(self.panel, -1, 

            "Bar width (%): ")

        self.slider_width = wx.Slider(self.panel, -1, 

            value=20, 

            minValue=1,

            maxValue=100,

            style=wx.SL_AUTOTICKS | wx.SL_LABELS)

        #self.slider_width.SetTickFreq(10, 1)

        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_width, self.slider_width)



        # Create the navigation toolbar, tied to the canvas

        #

        self.toolbar = NavigationToolbar(self.canvas)

        

        #

        # Layout with box sizers

        #

        

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.vbox.Add(self.toolbar, 0, wx.EXPAND)

        self.vbox.AddSpacer(10)

        

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL

        self.hbox.Add(self.RSIStaticTxt, 0, border=3, flag=flags)
        self.hbox.Add(self.RSITextbox, 0, border=3, flag=flags)

        self.hbox.Add(self.tradebutton, 0, border=3, flag=flags)

        self.hbox.Add(self.cb_grid, 0, border=3, flag=flags)

        self.hbox.AddSpacer(30)

        self.hbox.Add(self.slider_label, 0, flag=flags)

        self.hbox.Add(self.slider_width, 0, border=3, flag=flags)

        

        self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP)

        

        self.panel.SetSizer(self.vbox)

        self.vbox.Fit(self)

    

    def create_status_bar(self):

        self.statusbar = self.CreateStatusBar()



    def draw_figure(self):

        """ Redraws the figure

        """

        str = self.RSITextbox.GetValue()

        self.data = list(map(int, str.split()))

        x = range(len(self.data))



        # clear the axes and redraw the plot anew

        #

        #self.axes.clear()        

        #self.axes.grid(self.cb_grid.IsChecked())

        

        #self.axes.bar(

        #    left=x, 

        #    height=self.data, 

        #    width=self.slider_width.GetValue() / 100.0, 

        #    align='center', 

         #   alpha=0.44,

         #   picker=5)

        

        self.canvas.draw()

    

    def on_cb_grid(self, event):

        self.draw_figure()

    

    def on_slider_width(self, event):

        self.draw_figure()

    

    def on_trade_button(self, event):
        str = self.RSITextbox.GetValue()
        
        self.rsiAlgorithm=RSIAlgorithm(intervalMin=5)
        self.rsiAlgorithm.setRSILevel(float(str))
        self.broker = GUITradeBroker(data = self.data, totalMoney=11000, invest=10000, algorithm = self.rsiAlgorithm)
        #self.broker.updateAlgorithm(self.rsiAlgorithm)
        #self.draw_figure()
        self.broker.trade()
        arr = self.broker.getEquityArr()
        fillcolor = 'darkgoldenrod'
        self.ax1.clear()
        textsize = 9
        self.ax1.text(0.025, 0.95, 'Equity', va='top', transform=self.ax1.transAxes, fontsize=textsize)
        self.ax1.plot(arr, color=fillcolor)
        
        
        self.ax2.clear()
        self.ax2.text(0.025, 0.95, 'Price', va='top', transform=self.ax2.transAxes, fontsize=textsize)
        self.ax2.plot(self.broker.getPriceArr(), color=fillcolor)
 
        self.ax3.clear()
        self.ax3.text(0.025, 0.95, 'RSI', va='top', transform=self.ax3.transAxes, fontsize=textsize)
        self.ax3.plot(self.broker.getRSIArr(), color=fillcolor)

        bsVec=[]
        annoVec=self.broker.getAnnoArr()
        for i in range(0, len(annoVec)):
            if annoVec[i] is 'b':
                bsVec.append(10)
            else:
                if annoVec[i] is 's':
                    bsVec.append(100)
                else:
                    bsVec.append(0)
        
        self.ax4.clear()
        self.ax4.text(0.025, 0.95, 'Buy / Sell', va='top', transform=self.ax4.transAxes, fontsize=textsize)
        self.ax4.plot(bsVec, color=fillcolor)

        
        self.canvas.draw()

    def on_pick(self, event):

        # The event received here is of the type

        # matplotlib.backend_bases.PickEvent

        #

        # It carries lots of information, of which we're using

        # only a small amount here.

        # 

        box_points = event.artist.get_bbox().get_points()

        msg = "You've clicked on a bar with coords:\n %s" % box_points

        

        dlg = wx.MessageDialog(

            self, 

            msg, 

            "Click!",

            wx.OK | wx.ICON_INFORMATION)



        dlg.ShowModal() 

        dlg.Destroy()        

    

    def on_text_enter(self, event):

        self.draw_figure()


    def on_save_plot(self, event):

        file_choices = "PNG (*.png)|*.png"

        

        dlg = wx.FileDialog(

            self, 

            message="Save plot as...",

            defaultDir=os.getcwd(),

            defaultFile="plot.png",

            wildcard=file_choices,

            style=wx.SAVE)

        

        if dlg.ShowModal() == wx.ID_OK:

            path = dlg.GetPath()

            self.canvas.print_figure(path, dpi=self.dpi)

            self.flash_status_message("Saved to %s" % path)

        

    def on_exit(self, event):

        self.Destroy()

        

    def on_about(self, event):

        msg = """ A demo using wxPython with matplotlib:

        

         * Use the matplotlib navigation bar

         * Add values to the text box and press Enter (or click "Draw!")

         * Show or hide the grid

         * Drag the slider to modify the width of the bars

         * Save the plot to a file using the File menu

         * Click on a bar to receive an informative message

        """

        dlg = wx.MessageDialog(self, msg, "About", wx.OK)

        dlg.ShowModal()

        dlg.Destroy()

    

    def flash_status_message(self, msg, flash_len_ms=1500):

        self.statusbar.SetStatusText(msg)

        self.timeroff = wx.Timer(self)

        self.Bind(

            wx.EVT_TIMER, 

            self.on_flash_status_off, 

            self.timeroff)

        self.timeroff.Start(flash_len_ms, oneShot=True)

    

    def on_flash_status_off(self, event):

        self.statusbar.SetStatusText('')





if __name__ == '__main__':

    #app = wx.PySimpleApp()
    app = wx.App()

    app.frame = MatPlotWxDisplay()

    app.frame.Show()

    app.MainLoop()