# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, OPERAND, EOF = 'INTEGER', 'OPERAND', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text.replace(' ', '')
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+' or current_char == '-' or current_char == '*' or current_char == '/':
            token = Token(OPERAND, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = [self.current_token]
        self.eat(INTEGER)

        while self.current_token.type == INTEGER:
            left.append(self.current_token)
            self.eat(INTEGER)

        # we expect the current token to be a '+' token
        op = self.current_token
        self.eat(OPERAND)

        # we expect the current token to be a single-digit integer
        right = [self.current_token]
        self.eat(INTEGER)

        while self.current_token.type == INTEGER:
            right.append(self.current_token)
            self.eat(INTEGER)
        result = calc_result(list2digit(left), list2digit(right), op.value)

        while self.current_token.type != EOF:
            left = result
            op = self.current_token
            self.eat(OPERAND)

            # we expect the current token to be a single-digit integer
            right = [self.current_token]
            self.eat(INTEGER)

            while self.current_token.type == INTEGER:
                right.append(self.current_token)
                self.eat(INTEGER)
            result = calc_result(left, list2digit(right), op.value)
        return result

def calc_result(l, r, op):
    if op == '+':
        return l+r
    elif op == '-':
        return l-r
    elif op == '*':
        return l*r
    elif op == '/':
        return l/r
    else:
        raise Exception("Unsupported Operand")
def list2digit(lisst):
    result = 0
    for i, num in enumerate(reversed(lisst)):
        result += num.value*(10**i)
    return result

def main():
    while True:
        try:
            try:
                text = raw_input('calc> ')
            except NameError:  # Python3
                text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()