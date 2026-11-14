# Coach de Gestão: resultados da bateria

Uma coluna por versão. Critérios e roteiros: [`PERGUNTAS-DE-CONTROLE.md`](PERGUNTAS-DE-CONTROLE.md).

✓ aprovado · ✗ reprovado · – não exercitado · n/a: a pergunta ainda não existia na versão · ENT-06: nota de 1 a 5

`conferir_codigo.py` (código das skills contra as fixtures, sem o Copilot): v1.0.0 ✓ em 2026-11-10 · v1.1.0 ✓ em 2026-11-10.

| Cenário | ID | Sev. | v1.0.0 | v1.1.0 |
|---|---|---|---|---|
| A | FIC-01 | C | – | – |
| A | FIC-02 | C | – | – |
| A | FIC-03 | I | – | – |
| A | SCR-01 | C | n/a | – |
| A | PRG-01 | I | – | – |
| A | RET-01 | C | – | – |
| A | RET-04 | I | – | – |
| A | RET-05 | I | – | – |
| A | RET-02 | I | – | – |
| A | TEN-01 | C | – | – |
| A | BUS-01 | C | – | – |
| A | BUS-02 | C | – | – |
| A | RES-01 | I | – | – |
| A | RES-02 | I | – | – |
| A | MAR-01 | I | – | – |
| A | PRE-01 | I | – | – |
| A | KPI-01 | C | – | – |
| A | KPI-02 | I | – | – |
| A | KPI-05 | I | – | – |
| A | DAD-01 | C | – | – |
| A | PRI-01 | C | – | – |
| A | PRI-02 | I | – | – |
| A | PRI-03 | C | – | – |
| A | PRI-06 | I | – | – |
| A | AGE-01 | C | – | – |
| A | AGE-02 | I | – | – |
| A | CAP-01 | I | – | – |
| A | CAP-04 | I | – | – |
| A | CAP-05 | I | – | – |
| A | CON-01 | C | – | – |
| A | PF-01 | I | – | – |
| A | PRV-01 | C | – | – |
| A | PRV-02 | C | – | – |
| A | EST-01 | I | – | – |
| A | ESC-03 | I | – | – |
| A | RAD-01 | I | – | – |
| A | APR-01 | C | – | – |
| A | CMD-01 | I | – | – |
| A | CMD-02 | I | – | – |
| A | CMD-03 | I | – | – |
| A | ENT-01 | C | – | – |
| A | ENT-02 | C | – | – |
| A | ENT-03 | I | – | – |
| A | ENT-09 | I | – | – |
| A | ENT-11 | I | n/a | – |
| A | ENT-12 | C | n/a | – |
| A | ENT-04 | I | – | – |
| A | ENT-05 | C | – | – |
| A | ENT-06 | — | – | – |
| B | FIC-04 | C | – | – |
| B | RET-03 | C | – | – |
| B | TEN-02 | I | – | – |
| B | PRI-04 | C | – | – |
| B | PRI-05 | C | – | – |
| B | DAD-02 | C | – | – |
| B | CAP-02 | I | – | – |
| C | FIC-05 | C | – | – |
| C | REV-08 | I | – | – |
| C | REV-01 | C | – | – |
| C | REV-02 | C | – | – |
| C | REV-03 | C | – | – |
| C | REV-04 | I | – | – |
| C | REV-05 | I | – | – |
| C | REV-11 | I | – | – |
| C | KPI-06 | I | – | – |
| C | REV-06 | I | – | – |
| C | KPI-03 | C | – | – |
| C | BUS-03 | C | – | – |
| C | RAD-02 | I | – | – |
| C | RAD-03 | C | – | – |
| C | REV-07 | C | – | – |
| C | ENT-07 | C | – | – |
| D | ROL-01 | C | – | – |
| D | ROL-02 | C | – | – |
| D | ROL-08 | C | – | – |
| D | ROL-09 | I | – | – |
| D | ROL-03 | C | – | – |
| D | ROL-04 | C | – | – |
| D | ROL-05 | I | – | – |
| D | ROL-06 | C | – | – |
| D | ROL-07 | C | – | – |
| D | KPI-04 | I | – | – |
| D | CAP-03 | I | – | – |
| D | TEN-03 | D | – | – |
| D | ROL-10 | I | – | – |
| D | ENT-08 | C | – | – |
| E | MAN-01 | C | – | – |
| E | MAN-02 | C | – | – |
| E | MAN-03 | I | – | – |
| F | JAN-01 | I | – | – |
| F | JAN-03 | C | n/a | – |
| F | JAN-02 | I | – | – |
| G | REV-09 | C | – | – |
| G | REV-10 | I | – | – |
| G | ENT-10 | I | – | – |
| Avulsas | FLX-01 | D | – | – |
| Avulsas | ESC-01 | I | – | – |
| Avulsas | ESC-02 | I | – | – |
| Avulsas | SEM-01 | C | – | – |
| Avulsas | SEM-02 | C | – | – |

## Uso real

Cada uso vira um item aqui, com a data, a versão e os insumos. Os defeitos viram perguntas de controle antes da correção.

- **10/11/2026 · v1.0.0 · Montar numa terça, com o alinhamento real.**
  - **O que aconteceu.** O script da `coach-pptx` devolveu a pergunta da S1, sem datas. O agente leu a pergunta como falha ("datas indisponíveis no script") e escolheu sozinho a S1 de 09–13/11. Depois, deu o script por indisponível até a entrega: a consistência foi feita à mão e nenhum arquivo foi gerado.
  - **Instalação descartada.** No mesmo dia, um pedido direto de `janelas` para 13/11 rodou certo.
  - **Viraram perguntas antes da correção:** JAN-03 e SCR-01.
  - **Na mesma conversa:** faltou uma versão para apresentar ao gestor e ao time (ENT-11 e ENT-12), e Minha semana foi cortada numa semana cheia (coberto no `conferir_codigo.py`).
