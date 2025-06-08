import pyttsx3

def falar_texto(texto):
	engine = pyttsx3.init()
	engine.setProperty('rate', 150)

    # Listar vozes disponíveis
	for voz in engine.getProperty('voices'):
		print(voz.id)

    # Tentar selecionar uma voz em português
	for voz in engine.getProperty('voices'):
		if 'brazil' in voz.id.lower():
			print(voz.id)
			engine.setProperty('voice', voz.id)
			break
			
	# engine.getProperty('voice')

	engine.say(texto)
	engine.runAndWait()

if __name__ == '__main__':
	falar_texto("Isso é um teste de síntese de voz em português.")