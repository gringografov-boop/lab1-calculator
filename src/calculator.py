import re
import sys
import warnings


class Calculator:
    def __init__(self):
        self.precedence = {
            '+':1, '-':1,
            '*':2, '/':2, '//':2, '%':2,
            '**':3,
            'unary+':4, 'unary-':4
        }
        self.assoc = {
            '+':'left','-':'left','*':'left','/':'left',
            '//':'left','%':'left','**':'right',
            'unary+':'right','unary-':'right'
        }

    def tokenize(self, expr):
        if not expr or not expr.strip():
            raise ValueError("Пустое выражение")
            
        expr_nospace = ''.join(ch for ch in expr if ch != ' ')
        index_map = [i for i, ch in enumerate(expr) if ch != ' ']
        pattern = re.compile(r'(?P<number>\d*\.\d+|\d+)|(?P<op>\*\*|//|[+\-*/%()])')
        tokens = []
        pos = 0
        for m in pattern.finditer(expr_nospace):
            if m.start() != pos:
                badpos = index_map[pos] if pos < len(index_map) else len(expr)-1
                raise ValueError(f"Неподдерживаемый символ в позиции {badpos}: '{expr[badpos]}'")
            if m.lastgroup == 'number':
                n = float(m.group())
                if abs(n) > sys.float_info.max:
                    raise OverflowError("Число слишком велико")
                tokens.append(('NUMBER', n))
            else:
                op = m.group()
                if op == '(':
                    tokens.append(('LPAREN', op))
                elif op == ')':
                    tokens.append(('RPAREN', op))
                else:
                    tokens.append(('OP', op))
            pos = m.end()
        if pos != len(expr_nospace):
            badpos = index_map[pos] if pos < len(index_map) else len(expr)-1
            raise ValueError(f"Неподдерживаемый символ в позиции {badpos}: '{expr[badpos]}'")

        out = []
        for i, (t, v) in enumerate(tokens):
            if t == 'OP' and v in '+-' and (i == 0 or out and out[-1][0] in ['OP', 'LPAREN']):
                out.append(('UNARY', 'unary'+v))
            else:
                out.append((t, v))
        return out

    def to_rpn(self, tokens):
        out = []
        st = []
        for t, v in tokens:
            if t == 'NUMBER':
                out.append(v)
            elif t in ['OP', 'UNARY']:
                while st and st[-1] != '(' and self._pop(st[-1], v):
                    out.append(st.pop())
                st.append(v)
            elif t == 'LPAREN':
                st.append(v)
            elif t == 'RPAREN':
                while st and st[-1] != '(':
                    out.append(st.pop())
                if not st:
                    raise ValueError("Несбалансированные скобки")
                st.pop()
        while st:
            if st[-1] in '()':
                raise ValueError("Несбалансированные скобки")
            out.append(st.pop())
        return out

    def _pop(self, a, b):
        pa = self.precedence[a]
        pb = self.precedence[b]
        return pa > pb if self.assoc[b] == 'right' else pa >= pb

    def eval_rpn(self, rpn):
        st = []
        for tok in rpn:
            if isinstance(tok, (int, float)):
                st.append(tok)
            elif isinstance(tok, str) and tok.startswith('unary'):
                if not st:
                    raise ValueError("Недостаточно операндов")
                x = st.pop()
                st.append(+x if tok == 'unary+' else -x)
            else:
                if len(st) < 2:
                    raise ValueError("Недостаточно операндов")
                b = st.pop()
                a = st.pop()
                st.append(self._op(a, b, tok))
        if len(st) != 1:
            raise ValueError("Неверное выражение")
        return st[0]

    def _op(self, a, b, op):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if b == 0: raise ZeroDivisionError("Деление на ноль")
            return a / b
        if op == '**':
            if a == 0 and b < 0:
                raise ZeroDivisionError("0 в отрицательной степени")
            return a ** b
        if op == '//':
            if b == 0: raise ZeroDivisionError("Деление на ноль")
            return a // b
        if op == '%':
            if b == 0: raise ZeroDivisionError("Деление на ноль")
            return a % b
        raise ValueError(f"Неизвестный оператор {op}")

    def calculate(self, expr):
        return self.eval_rpn(self.to_rpn(self.tokenize(expr)))
