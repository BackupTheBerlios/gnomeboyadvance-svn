import os.path
import gtk
import gobject

from const import DATADIR, LOGOFILE

class GameList:
	def __init__(self, gladeHandler):
		self.gameList = gladeHandler.get_widget("gameList")
		self.gameCount = gladeHandler.get_widget("gameCount")
		self.gameImage = gladeHandler.get_widget("gameImage")

		self.captureDir = None
		self.theGame = None
		self.gamesDict = []
		self.gameListModel = gtk.ListStore(gobject.TYPE_STRING)
		self.col = gtk.TreeViewColumn("Game",gtk.CellRendererText(),text=0)
		self.selection = self.gameList.get_selection()

		self.gameList.set_model(self.gameListModel)
		self.col.set_sort_column_id(0)
		self.gameList.append_column(self.col)
		self.selection.set_mode('single')
		self.selection.connect('changed' ,self.selectGame)
		

		

        def populate(self, romsDir, tosearch=''):
                if tosearch:
                       tosearch = tosearch.lower()

		self.gameListModel.clear()
		if os.path.isdir(romsDir):
			self.gamesDict = os.listdir(romsDir)
		else:
			print romsDir + ' is not a directory.'
		gameCount = 0
		for eachGame in self.gamesDict:
			if (eachGame[-3:].lower() in ['zip','gba']) and (eachGame.lower().find(tosearch) != -1):
				iter = self.gameListModel.append()
				self.gameListModel.set_value(iter,0,eachGame)
				gameCount += 1

		self.gameCount.set_text('Total roms : ' + `gameCount`)

	def selectGame(self, selection):
		sel = selection.get_selected()

		if sel:
			model, iter = sel
			if iter:
				module = model.get_value(iter, 0)
				self.theGame = model.get_value(iter,0)
			else:
				self.theGame = None

		if os.path.isdir(self.captureDir):
			theImage = os.path.join(self.captureDir, self.theGame[:-4] + '01.png')
			if os.path.isfile(theImage):
				self.gameImage.set_from_file(theImage)
			else:
				self.gameImage.set_from_file( os.path.join(DATADIR, LOGOFILE))
		#app.appBar.set_status(theGame)

