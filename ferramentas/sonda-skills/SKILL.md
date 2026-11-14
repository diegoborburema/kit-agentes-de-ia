---
name: sonda-skills
description: 'Diagnóstico do ambiente onde rodam os scripts das skills: roda scripts/sonda.py e mostra o resultado sem resumir. Use só quando o usuário pedir "rodar sonda".'
---

Quando o usuário pedir **"rodar sonda"**, faça estes 4 passos, sem pular e sem interpretar:

1. Rode o script `scripts/sonda.py` desta skill, sem alterar nada. Mostre a saída **completa** num bloco de código.
2. Se o script gravar um arquivo `.pptx`, ofereça o link de download.
3. No interpretador de código, rode este trecho e mostre a saída completa, trocando `<CAMINHO>` pelo caminho de `sonda.py` que a sonda imprimiu na linha `== __file__`:

~~~python
import os
print("cwd:", os.getcwd())
print("arquivos:", os.listdir("."))
try:
    print(open("<CAMINHO>", encoding="utf-8").read()[:120])
    print("LEITURA DO SCRIPT PELO INTERPRETADOR: OK")
except Exception as e:
    print("LEITURA DO SCRIPT PELO INTERPRETADOR: FALHOU", type(e).__name__, e)
try:
    import pptx
    print("python-pptx no interpretador:", pptx.__version__)
except Exception as e:
    print("python-pptx no interpretador: FALHOU", e)
~~~

4. Diga, em uma linha cada: (a) que ferramenta rodou o passo 1 (o script da skill ou o interpretador de código); (b) se o arquivo anexado na mensagem apareceu para o script.

Não corrija nem reescreva o script. Se algo falhar, mostre o erro como veio.
