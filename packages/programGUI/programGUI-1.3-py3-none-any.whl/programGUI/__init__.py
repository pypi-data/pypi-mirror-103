"""programGUI
"""
import PySimpleGUI as sg

__author__ = "help@castellanidavide.it"
__version__ = "01.03 2021-04-22"

class programGUI:
	def __init__ ( self, 
				   title="Test", 
				   instructions=[
						[{"type": "bool", "title": "Want you to run it in the verbose mode?", "id": "verbose"}],
						[{"type": "text", "title": "Insert text:", "id": "text"}],
						[{"type": "list", "title": "Choose from the list:", "id": "list", "options":["a", "b", "c"]}],
					]):
		window = None

		layout = []

		for col in instructions:
			temp = []
			for elem in col:
				if elem["type"] == "bool":
					temp.append([sg.Text(elem["title"])])
					temp.append([sg.Checkbox(elem["title"], default=False,key=elem["id"])])
				elif elem["type"] == "text":
					temp.append([sg.Text(elem["title"])])
					temp.append([sg.InputText(key=elem["id"])])
				elif elem["type"] == "list":
					temp.append([sg.Text(elem["title"])])
					temp.append([sg.Combo(elem["options"], size=(max(map(len, elem["options"]))+1, 5), key=elem["id"])])
			
			layout.append(sg.Column(temp))
			layout.append(sg.VSeperator())

		layout.append(sg.Column([
			[sg.Text("To start the code, please press two times the following button:")],
			[sg.Button("Start")],
		]))

		window = sg.Window(title, [layout])

		while True:
			input = window.read()[0]
			if input == "Start" or input == "Exit" or input == sg.WIN_CLOSED:
				break

		self.output = window.read()[1]
		window.close()

	def get_values(self):
		return self.output
		
if __name__ == "__main__":
	programGUI()
