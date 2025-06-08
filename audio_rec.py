import speech_recognition as sr
            
def interpretador_audio():
      return sr.Recognizer()

def microfone():
      return sr.Microphone()

def transcreve_audio(r, audio):
    try:
        texto = r.recognize_google(audio, language='pt-BR')
        print("Você disse:", texto)
        return texto
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
    except sr.RequestError as e:
        print(f"Erro ao requisitar resultados do serviço; {e}")

# Exemplo de uso:
if __name__ == "__main__":
    transcreve_audio()