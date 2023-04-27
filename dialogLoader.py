def load_dialog(dialogID):
	if dialogID == 1:
		return "Welcome to the store!\nI am selling health for 1 coin.\nPress E To Buy, R To close"
	elif dialogID == 0:
		return "Hello, welcome to my store.\nUnfortunately, I am out of stock.\nPlease Come back later.\nPress R or E to Close"
	elif dialogID == 2:
		return "^ Route to much pain \n https://tinyurl.com/ziggy2site"
	elif dialogID == 3:
		return "*passive agressive*\n Sorry, you are OUT of coins. \n Get a job like me and earn some! \n some people are just lucky... \n They find coins on the ground... ANYWAYS!\n Press R or E to close."
	elif dialogID == -1:
		return "Game Over! \n Press R or E to close."