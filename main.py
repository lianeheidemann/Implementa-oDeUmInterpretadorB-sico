import re

# +++++ LÉXICO +++++
tokens_def = [
    ('NUM', r'\d+(\.\d+)?'),
    ('SE', r'\bif\b'),
    ('SENAO', r'\belse\b'),
    ('MAIN', r'\bmain\b'),
    ('VAR', r'\bvar\b'),
    ('TIPO', r'\b(?:int|float|bool)\b'),
    ('LOG', r'\b(?:and|or|not)\b'),
    ('COMP', r'==|!=|>=|<=|>|<'),
    ('ATRIB', r'='),
    ('FIM', r';'),
    ('OP', r'[\+\-\*/]'),
    ('APAR', r'\('),
    ('FPAR', r'\)'),
    ('ACH', r'\{'),
    ('FCH', r'\}'),
    ('DOISPONTOS', r':'),
    ('ID', r'[A-Za-z_]\w*'),
    ('IGNORA', r'[ \t\n]+'),
    ('ERRO', r'.'),
]

master_re = re.compile('|'.join(f'(?P<{t}>{p})' for t, p in tokens_def))

def lexer(codigo):
    for m in master_re.finditer(codigo):
        tipo, val = m.lastgroup, m.group()
        if tipo == 'IGNORA': continue
        if tipo == 'ERRO': raise RuntimeError(f"Caractere inválido: {val!r}")
        yield tipo, val

# +++++ INTERPRETADOR +++++
class Interpretador:
    def __init__(self):
        self.vars = {}
        self.tokens = []
        self.pos = 0

    def executar(self, tokens):
        self.tokens, self.pos = list(tokens), 0
        while self.pos < len(self.tokens):
            self.comando()

    def ver(self, t): 
        return self.pos < len(self.tokens) and self.tokens[self.pos][0] == t

    def pega(self, t):
        if not self.ver(t):
            raise RuntimeError(f"Esperado {t}, encontrado {self.tokens[self.pos][1]!r}")
        self.pos += 1
        return self.tokens[self.pos-1][1]

    # COMANDOS
    def comando(self):
        if self.ver('VAR'): self.declaracao()
        elif self.ver('ID') and (self.pos+1 < len(self.tokens)) and self.tokens[self.pos+1][0] == 'ATRIB':
            self.atribuicao()
        elif self.ver('MAIN'): self.bloco()
        elif self.ver('SE'): self.condicional()
        else: self.pos += 1

    def declaracao(self):
        self.pega('VAR')
        nome = self.pega('ID')
        if self.ver('DOISPONTOS'): self.pega('DOISPONTOS')
        self.pega('TIPO')
        
        val = None
        if self.ver('ATRIB'):
            self.pega('ATRIB')  # pega '=' primeiro
            val = self.expr()    # depois avalia a expressão
        
        self.pega('FIM')
        self.vars[nome] = val

    def atribuicao(self):
        nome = self.pega('ID')
        self.pega('ATRIB')
        val = self.expr()
        self.pega('FIM')
        self.vars[nome] = val

    def bloco(self):
        self.pega('MAIN'); self.pega('ACH')
        while not self.ver('FCH'): self.comando()
        self.pega('FCH')

    def condicional(self):
        self.pega('SE'); cond = self.expr(); self.pega('ACH')
        if cond:
            while not self.ver('FCH'): self.comando()
            self.pega('FCH')
            if self.ver('SENAO'):
                self.pega('SENAO'); self.pega('ACH'); self.descarta_bloco()
        else:
            self.descarta_bloco()
            if self.ver('SENAO'):
                self.pega('SENAO'); self.pega('ACH')
                while not self.ver('FCH'): self.comando()
                self.pega('FCH')

    def descarta_bloco(self):
        depth = 1
        while depth > 0:
            if self.ver('ACH'): depth += 1
            elif self.ver('FCH'): depth -= 1
            self.pos += 1

    # EXPRESSÕES
    def expr(self):
        v = self.termo_log()
        while self.ver('LOG') and self.tokens[self.pos][1] == 'or':
            self.pega('LOG'); v = v or self.termo_log()
        return v

    def termo_log(self):
        v = self.compara()
        while self.ver('LOG') and self.tokens[self.pos][1] == 'and':
            self.pega('LOG'); v = v and self.compara()
        return v

    def compara(self):
        v = self.arit()
        if self.ver('COMP'):
            op = self.pega('COMP'); d = self.arit()
            return eval(f"{v}{op}{d}")
        return v

    def arit(self):
        v = self.fator()
        while self.ver('OP') and self.tokens[self.pos][1] in '+-':
            op = self.pega('OP'); v = (v + self.fator()) if op=='+' else (v - self.fator())
        return v

    def fator(self):
        v = self.termo()
        while self.ver('OP') and self.tokens[self.pos][1] in '*/':
            op = self.pega('OP'); v = (v * self.termo()) if op=='*' else (v / self.termo())
        return v

    def termo(self):
        if self.ver('NUM'): return float(self.pega('NUM'))
        if self.ver('ID'):
            nome = self.pega('ID')
            if nome in self.vars: return self.vars[nome]
            raise RuntimeError(f"Variável não declarada: {nome}")
        if self.ver('APAR'): self.pega('APAR'); v = self.expr(); self.pega('FPAR'); return v
        if self.ver('LOG') and self.tokens[self.pos][1]=='not': self.pega('LOG'); return not self.termo()
        raise RuntimeError(f"Token inválido em expressão: {self.tokens[self.pos][1]!r}")

# +++++ TESTE +++++
if __name__ == "__main__":
    codigo = """
    var x:int = 10;
    var y:int = 5;
    var z:int = 0;

    main {
        x = x + 3;
        y = y * 2;

        if x > 10 {
            z = 1;
        } else {
            z = 2;
        }

        if y < 5 or z == 1 {
            x = x + 1;
        }
    }
    """
    interp = Interpretador()
    try:
        interp.executar(lexer(codigo))
        print("Estado final:", interp.vars)
    except RuntimeError as e:
        print("Erro de execução:", e)
