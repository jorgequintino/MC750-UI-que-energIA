# MC750-UI-que-energIA



## Autores
- [Ainaras Marão](https://github.com/MaraoLT)  (182338)
- [Douglas Henrique R. A. Pereira](https://github.com/Dourialp)  (245202)
- [Jorge Felipe L. Pereira](https://github.com/jorgequintino)  (251771)
- [Rafael Carro Gaudim](https://github.com/RafaelCarro)  (240879)
- [Yan Oliveira da Silva](https://github.com/Cl4nyz)  (236363)

Abra o terminal e navegue até a pasta do seu projeto.
Crie a venv:
```bash
python3 -m venv .venv
```
Ative a venv:
```bash
source .venv/bin/activate
```
Instale os pacotes necessários para execução do programa:
```bash
python app.py
```

Acesse em:
```bash
http://127.0.0.1:5000/
```

### Configurando a API da OpenAI

1. Crie uma conta em [https://platform.openai.com/signup](https://platform.openai.com/signup).
2. Após criar sua conta, acesse [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) e gere uma nova chave de API.
3. Copie o arquivo `.example.env` para `.env`:
   ```bash
   cp example.env .env
   ```
4. Abra o arquivo `.env` e cole sua chave de API no campo apropriado, por exemplo:
   ```
   OPENAI_API_KEY=sua-chave-aqui
   ```
5. Salve o arquivo `.env`. O programa irá carregar automaticamente sua chave ao rodar.

Pronto! Agora é só executar o programa `interface.py`!