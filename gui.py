def after_clicking(event):
    #wx.MessageBox("Sorry i am broke","click ok to buy me food")
    button1.SetLabel("no money")
def after_entering(event):
    print(event.GetString())
import wx
app=wx.App()
frame=wx.Frame(None,title="WELCOME",size=(500,500))
panel=wx.Panel(frame,style=wx.SIMPLE_BORDER)
panel.SetBackgroundColour("pink")
button1=wx.Button(panel,label="click for free food",pos=(200,200),size=(100,30))
button1.SetBackgroundColour("violet")
button1.Bind(wx.EVT_BUTTON,after_clicking)
textbox=wx.TextCtrl(panel,pos=(20,20))
textbox.Bind(wx.EVT_TEXT,after_entering)
frame.Show()
app.MainLoop()