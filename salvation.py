#!/usr/bin/python

'''
"Salvation" was created by Tatsu and Ransara.

Tatsu's Github: github.com/tatsuonline
Tatsu's Email Address: tatsu@tutanota.com

Ransara's Github: github.com/sransara
Ransara's Email Address: _____________

This is freedom respecting software (licsense: GPLv3). Change and share whatever you would like to!
'''

import os
import wxversion
wxversion.select('3.0')
import wx
import wx.lib.dialogs
import wx.stc as stc

# Fonts in dictionary structure
faces = {
    "times": "Times New Roman",
    "mono": "Courier New",
    "helvetica": "Arial",
    "other": "Comic Sans MS",
    "size": 10,
    "size2": 8
}

# The Main Window, baby.
class MainWindow(wx.Frame):
    def __init__(self, parent, title):

        # Current Directory and File Name
        self.dirname = ""
        self.filename = ""
        
        # Line Number Toggle
        self.lineNumbersEnabled = True

        # Command Mode
        self.commandMode = "salvation" # Default commands

        # Set Margin
        self.leftMarginWidth = 25

        # Appearance
        wx.Frame.__init__(self, parent, title = title, size=(800, 600))
        self.control = stc.StyledTextCtrl(self, style = wx.TE_MULTILINE | wx.TE_WORDWRAP)
        self.control.SetLexer(stc.STC_LEX_PYTHON)
        #self.control.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetBackgroundColour("BLUE")

        # Key Bindings
        self.control.CmdKeyAssign(ord("="), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN) # Zoom in (Ctrl and +)
        self.control.CmdKeyAssign(ord("-"), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT) # Zoom out (Ctrl and -)

        # Gets rid of whitespace
        self.control.SetViewWhiteSpace(False)

        # Set Line Numbers Column
        self.control.SetMargins(5, 0) # 5 pixels of space from the line numbers
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER) # Line Numbers
        self.control.SetMarginWidth(1, self.leftMarginWidth) # Line Numbers

        # Status Bar at bottom
        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))

        # File Menu
        filemenu = wx.Menu()
        menuNew = filemenu.Append(wx.ID_NEW, "&New", " Create a new document") # New Document
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open an existing document") # Open Document
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", " Save the current document") # Save Document
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save &As...", " Save a new document") # Save As
        filemenu.AppendSeparator() # It's a separator, yo.
        menuClose = filemenu.Append(wx.ID_EXIT, "&Close", " Close salvation") # Closes Salvation

        # Edit Menu
        editmenu = wx.Menu()
        menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", " Undo the last operation") # Undo
        menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", " Redo the last operation") # Redo
        editmenu.AppendSeparator() # It's a separator, yo.
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "&Select All", " Select all the things!") # SelectAll
        editmenu.AppendSeparator() # It's a separator, yo.
        menuCut = editmenu.Append(wx.ID_CUT, "&Cut", " Cut the selected text") # Cut
        menuCopy = editmenu.Append(wx.ID_COPY, "C&opy", " Copy the selected text") # Copy
        menuPaste = editmenu.Append(wx.ID_PASTE, "&Paste", " Paste from clipboard") # Paste

        # Preferences Menu
        prefmenu = wx.Menu()
        menuLinesToggle = prefmenu.Append(wx.ID_ANY, "&Toggle Line Numbers", " Show/Hide Line Numbers")

        # Mode Menu
        modemenu = wx.Menu()
        menuSalvationMode = modemenu.Append(wx.ID_ANY, "&salvation Command Mode", " Default commands")
        menuEmacsMode = modemenu.Append(wx.ID_ANY, "&Emacs Command Mode", " Use Emacs commands in salvation")
        menuViVimMode = modemenu.Append(wx.ID_ANY, "&Vi/Vim Command Mode", " Use Vi/Vim commands in salvation")
        
        # Help Menu
        helpmenu = wx.Menu()
        menuHowTo = helpmenu.Append(wx.ID_ANY, "&How To...", " Even the mighty need help") # Help
        helpmenu.AppendSeparator() # It's a separator, yo.
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About", " Curiosity never killed the programmer") # About
        
        # Add the Menu Bar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(prefmenu, "&Preferences")
        menuBar.Append(modemenu, "&Mode")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)

	# Add the Tool Bar
	#toolBar = wx.ToolBar()
	#self.SetToolBar(toolBar)

        # Event Binding
        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)

        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)

        self.Bind(wx.EVT_MENU, self.OnToggleLineNumbers, menuLinesToggle)

        self.Bind(wx.EVT_MENU, self.OnSalvationMode, menuSalvationMode)
        self.Bind(wx.EVT_MENU, self.OnEmacsMode, menuEmacsMode)
        self.Bind(wx.EVT_MENU, self.OnViVimMode, menuViVimMode)
        
        # Change Command Mode
        if self.commandMode == "salvation":
            self.control.Bind(wx.EVT_CHAR, self.OnSalvationCommand)
        elif self.commandMode == "Emacs":
            self.control.Bind(wx.EVT_CHAR, self.OnEmacsCommand)
        elif self.commandMode == "ViVim":
            self.control.Bind(wx.EVT_CHAR, self.OnViVimCommand)
        else:
            self.control.Bind(wx.EVT_CHAR, self.OnSalvationCommand) # Default Mode
        
        self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.control.Bind(wx.EVT_KEY_UP, self.OnLineCol)

        # Icon Setting
        ico = wx.Icon('/home/blah/Salvation/Logo.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        
        # Show salvation to the masses
        self.Show()

        # Show Dem Positions!
        self.OnLineCol(self)

        # Syntax Test
        # defaulting the style
	self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helvetica)s,size:%(size)d" % faces)
	self.control.StyleClearAll() # reset all to be like default

	# global default styles for all languages
	self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helvetica)s,size:%(size)d" % faces)
	self.control.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helvetica)s,size:%(size2)d" % faces)
	self.control.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
	self.control.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
	self.control.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")
        # Python styles
	# Default
        self.control.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helvetica)s,size:%(size)d" % faces)
	# Comments
	self.control.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
	# Number
	self.control.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
	# String
	self.control.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helvetica)s,size:%(size)d" % faces)
	# Single-quoted string
	self.control.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helvetica)s,size:%(size)d" % faces)
	# Keyword
	self.control.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
	# Triple quotes
	self.control.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
	# Triple double quotes
	self.control.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
	# Class name definition
	self.control.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
	# Function name definition
	self.control.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
	# Operators
	self.control.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
	# Identifiers
	self.control.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helvetica)s,size:%(size)d" % faces)
	# Comment blocks
	self.control.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
	# End of line where string is not closed
	self.control.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

	self.control.SetCaretForeground("ORANGE")
        
    # File Menu Events
        
    def OnNew(self, event): # New File
        self.filename = ""
        self.control.SetValue("")

    def OnOpen(self, event): # Open File
        try:
            dialogBox = wx.FileDialog(self, "Choose A File", self.dirname, "", "*.*", wx.FD_OPEN)
            if dialogBox.ShowModal() == wx.ID_OK:
                self.filename = dialogBox.GetFilename()
                self.dirname = dialogBox.GetDirectory()
                filer = open(os.path.join(self.dirname, self.filename), "r")
                self.control.SetValue(filer.read())
                filer.close()
            dialogBox.Destroy()
        except:
            dialogBox = wx.FileMessage(self, "Oh noes! The file couldn't be opened!", "Error", wx.ICON_ERROR)
            dialogBox.ShowModal()
            dialogBox.Destroy()

    def OnSave(self, event): # Save File
        try:
            filer = open(os.path.join(self.dirname, self.filename), "w")
            filer.write(self.control.GetValue())
            filer.close()
        except:
            try:
                dialogBox = wx.FileDialog(self, "Save File As", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dialogBox.ShowModal() == wx.ID_OK:
                    self.filename = dialogBox.GetFilename()
                    self.dirname = dialogBox.GetDirectory()
                    filer = open(os.path.join(self.dirname, self.filename), "w")
                    filer.write(self.control.GetValue())
                    filer.close()
                dialogBox.Destroy()
            except:
                dialogBox = wx.FileMessage(self, "Oh noes! The file couldn't be saved!", "Error", wx.ICON_ERROR)
            dialogBox.ShowModal()
            dialogBox.Destroy()

    def OnSaveAs(self, event): # Save As
        try:
            filer = open(os.path.join(self.dirname, self.filename), "w")
            filer.write(self.control.GetValue())
            filer.close()
        except:
            try:
                dialogBox = wx.FileDialog(self, "Save File As", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dialogBox.ShowModal() == wx.ID_OK:
                    self.filename = dialogBox.GetFilename()
                    self.dirname = dialogBox.GetDirectory()
                    filer = open(os.path.join(self.dirname, self.filename), "w")
                    filer.write(self.control.GetValue())
                    filer.close()
                dialogBox.Destroy()
            except:
                dialogBox = wx.FileMessage(self, "Oh noes! The file couldn't be saved!", "Error", wx.ICON_ERROR)
            dialogBox.ShowModal()
            dialogBox.Destroy()

    def OnClose(self, event): # Close Everything
        self.Close(True)

    # Edit Menu Events

    def OnUndo(self, event): # Undo Event
        self.control.Undo()

    def OnRedo(self, event): # Redo Event
        self.control.Redo()
        
    def OnSelectAll(self, event): # Select All Event
        self.control.SelectAll()    

    def OnCut(self, event): # Cut Event
        self.control.Cut()

    def OnCopy(self, event): # Copy Event
        self.control.Copy()

    def OnPaste(self, event): # Paste Event
        self.control.Paste()

    # Preferences Events

    def OnToggleLineNumbers(self, event): # Toggle Line Numbers Event
        if self.lineNumbersEnabled == True:
            self.control.SetMarginWidth(1, 0)
            self.lineNumbersEnabled = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnabled = True

    # Help Events

    def OnHowTo(self, event): # How To Event
        filer = open("shortcuts.txt", "r")
	message = filer.read()
	filer.close()
        dialogBox = wx.lib.dialogs.ScrolledMessageDialog(self, message, "How To Be Awesome", size = (400, 400))
        dialogBox.ShowModal()
        dialogBox.Destroy()

    def OnAbout(self, event): # About Event
        dialogBox = wx.lib.dialogs.ScrolledMessageDialog(self, "Salvation Saves Lives", "About", size = (400, 400))
        dialogBox.ShowModal()
        dialogBox.Destroy()

    # Line + Column Display Event
    def OnLineCol(self, event):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
	filer = self.filename
        currentPosition = " Line %s, Column %s... and yet, lost in your code.   |   Current file: %s" % (line, col, filer)
        self.StatusBar.SetStatusText(currentPosition, 0)

    # Filename Display
    #def OnFileDisplay(self, event):
	#filer = self.filename
	#display = "  Current file: %s" % (filer)
	#self.StatusBar.SetStatusText(display, 20)

    # Modes
    def OnSalvationMode(self, event):
        self.commandMode = "salvation"
        #print "salvation mode"

    def OnEmacsMode(self, event):
        self.commandMode = "Emacs"
        #print "Emacs mode"

    def OnViVimMode(self, event):
        self.commandMode = "ViVim"
        #print "ViVim mode"
        
    # Salvation Commands
    def OnSalvationCommand(self, event):
        keycode = event.GetKeyCode()
        altdown = event.AltDown()
        #print keycode
        if keycode == 14: # Ctrl + N
            self.OnNew(self)
        elif keycode == 15: # Ctrl + O
            self.OnOpen(self)
        elif keycode == 19: # Ctrl + S
            self.OnSave(self)
        elif altdown and keycode == 115: # Alt + S
            self.OnSaveAs(self)
        elif keycode == 17: # Ctrl + Q
            self.OnClose(self)
        elif keycode == 340: # F1
            self.OnHowTo(self)
        elif keycode == 341: # F2
            self.OnAbout(self)
        else:
            event.Skip()

    # Emacs Commands
    def OnEmacsCommand(self, event):
        keycode = event.GetKeyCode()
        altdown = event.AltDown()
        if keycode == 14: # Ctrl + N
            self.OnOpen(self)
        elif keycode == 15: # Ctrl + O
            self.OnOpen(self)
        elif keycode == 19: # Ctrl + S
            self.OnSave(self)
        elif altdown and keycode == 115: # Alt + S
            self.OnSaveAs(self)
        elif keycode == 17: # Ctrl + Q
            self.OnClose(self)
        elif keycode == 340: # F1
            self.OnHowTo(self)
        elif keycode == 341: # F2
            self.OnAbout(self)
        else:
            event.Skip()

    # ViVim Commands
    def OnViVimCommand(self, event):
        keycode = event.GetKeyCode()
        altdown = event.AltDown()
        if keycode == 14: # Ctrl + N
            self.OnNew(self)
        elif keycode == 15: # Ctrl + O
            self.OnOpen(self)
        elif keycode == 19: # Ctrl + S
            self.OnSave(self)
        elif altdown and keycode == 115: # Alt + S
            self.OnSaveAs(self)
        elif keycode == 17: # Ctrl + Q
            self.OnClose(self)
        elif keycode == 340: # F1
            self.OnHowTo(self)
        elif keycode == 341: # F2
            self.OnAbout(self)
        else:
            event.Skip()
            
app = wx.App()
frame = MainWindow(None, "salvation")
app.MainLoop()
