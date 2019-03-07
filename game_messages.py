import libtcodpy as libtcod

import textwrap

class Message:
    def __init__(self,text,color=libtcod.white):
	    self.text = text
	    self.color = color

class MessageLog:
	def __init__(self,x,width,height):
	    self.messages=[]
	    self.x=x
	    self.width=width
	    self.height=height

	def add_message(self,message):
		#split the mesage if necessary, among multiple lines
		new_msg_line = textwrap.wrap(message.text, self.width)

		for line in new_msg_line:   # If the buffer is full, remove the first line to make room for the new one 
			if len(self.messages)==self.height:
				del self.messages[0]
            # Add the new line as a Message object, with the text and the color  
			self.messages.append(Message(line,message.color))

