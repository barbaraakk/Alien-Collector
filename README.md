# Alien Collector 👾

Um pequeno jogo **point-and-click** feito em **Python com PgZero**, criado para o teste prático.  
O objetivo é coletar todos os cristais enquanto evita as abelhas inimigas!

---

## 🎮 Como jogar
- Clique com o **mouse** em qualquer ponto do cenário para mover o Alien.
- Colete todos os cristais brilhantes 💎.
- Se uma abelha tocar em você 🐝 → Game Over.
- Ao coletar tudo, o próximo nível começa automaticamente.

---

## 🧱 Recursos implementados
- Menu principal com botões clicáveis:
  - **Iniciar**
  - **Som On/Off**
  - **Sair**
- Música de fundo e efeitos sonoros.
- Vários inimigos.
- Animação de sprites (idle e movimento).
- Sistema de pontuação e transição de níveis.
- Códigos e nomes seguindo PEP8 e boas práticas.

---

## 🧩 Bibliotecas utilizadas
Apenas:
- **pgzero**
- **math**
- **random**
- `Rect` importado do módulo `pygame`.

---

## 🗂️ Estrutura
```
game/
├── main.py
├── images/
├── sounds/
├── music/
└── README.md
```
---

## 🚀 Como executar
1. Instale o Python 3.10+
2. Instale o PgZero:
   ```bash
   pip install pgzero
3. Execute o jogo:
   ```bash
    pgzrun main.py

