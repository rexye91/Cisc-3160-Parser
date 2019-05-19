
def main():
    """
    Do some tests
    """
    expr = input("Enter an expression: ")

    variables = dict()

    if parse_program(expr, variables):
        for variable, value in variables.items():
            print(variable + " = " + str(value))
    else:
        print("error")


def parse_program(expr, variables):
    """
    Program -> Assignment*
    """
    while len(expr) > 0:
        expr = parse_assignment(expr, variables)

        if expr is False:
            return False

    # If all letters has been consumed then it is a valid expression
    return True


def parse_assignment(expr, variables):
    """
    Assignment -> Identifier = Exp;
    :param expr:
    :return:
    """
    expr = expr.lstrip()

    # Find an identifier
    new_expr, identifier = parse_identifier(expr)

    # Assignment fails if it doesn't start with an identifier
    if new_expr is False:
        return False

    # If identifier found, we should expect an '=' next
    expr = new_expr.lstrip()
    if expr[0] != '=':
        return False

    expr = expr[1:]

    # After an equal sign we parse an expression
    new_expr, value = parse_expression(expr, variables)

    if new_expr is False:
        return False

    # Expect a semi-colon next
    expr = new_expr.lstrip()

    if expr.startswith(';'):
        variables[identifier] = value
        return expr[1:]

    return False


def parse_expression(expr, variables):
    """
    Exp -> Exp + Term | Exp - Term | Term
    The grammar results to infinite recursion thus we need to modify as:
    Exp -> Term + Exp | Term - Expr | Term
    """
    expr = expr.lstrip()

    # Find the term
    expr, value = parse_term(expr, variables)

    if expr is not False:
        expr = expr.lstrip()

        # Find + Exp
        if expr.startswith("+"):
            new_expr, next_value = parse_expression(expr[1:], variables)
            if new_expr is not False:
                return new_expr, value + next_value

        # Find - Exp
        if expr.startswith("-"):
            new_expr, next_value = parse_expression(expr[1:], variables)
            if new_expr is not False:
                return new_expr, value - next_value

        return expr, value

    return False, None


def parse_term(expr, variables):
    """
    Term -> Term * Fact | Fact
    The grammar results to infinite recursion thus we need to modify as:
    Term -> Fact * Term | Fact
    """
    expr = expr.lstrip()

    # Find a fact
    expr, value = parse_fact(expr, variables)

    if expr is not False:
        expr = expr.lstrip()

        # Find * Term
        if expr.startswith("*"):
            new_expr, next_value = parse_term(expr[1:], variables)
            if new_expr is not False:
                return new_expr, value * next_value

        return expr, value

    return False, None


def parse_fact(expr, variables):
    """
    Fact -> (Exp) | -Fact | +Fact | Literal | Identifier
    """
    expr = expr.lstrip()

    # Test (Exp)
    if expr.startswith('('):
        new_expr, value = parse_expression(expr[1:], variables)
        if new_expr is not False and new_expr.startswith(')'):
            return new_expr[1:], value

    # Test -Fact or +Fact
    if expr.startswith('-') or expr.startswith('+'):
        new_expr, value = parse_fact(expr[1:], variables)
        if new_expr is not False:
            if expr.startswith('-'):
                return new_expr, -value
            else:
                return new_expr, value

    # Test literal
    new_expr, value = parse_literal(expr)

    if new_expr is not False:
        return new_expr, value

    # Test identifier
    new_expr, identifier = parse_identifier(expr)

    # Check that the identifier has been initialized
    if identifier not in variables.keys():
        print(identifier + " is not initialized")
        return False, None

    if new_expr is not False:
        return new_expr, variables[identifier]

    return False, None


def parse_literal(expr):
    """
    Literal -> 0 | NonZeroDigit Digit*
    NonZeroDigit -> 1..9
    Digit -> 0..9
    """
    expr = expr.lstrip()

    if expr.startswith('0'):
        return expr[1:], 0

    if len(expr) == 0 or not '1' <= expr[0] <= '9':
        return False, None

    literal = expr[0]
    expr = expr[1:]

    while len(expr) > 0 and '0' <= expr[0] <= '9':
        literal += expr[0]
        expr = expr[1:]

    return expr, int(literal)


def parse_identifier(expr):
    """
    Identifier -> Letter | [Letter | Digit]*
    Letter -> a..z | A..Z | _
    Digit -> 0..9
    """
    expr = expr.lstrip()

    # Identifiers are expected to start with a letter
    identifier = ""

    if not ('a' <= expr[0] <= 'z') and not ('A' <= expr[0] <= 'Z'):
        return False, None

    # The rest are letters or digit
    identifier += expr[0]
    expr = expr[1:]

    while len(expr) > 0:
        if 'a' <= expr[0] <= 'z' or 'A' <= expr[0] <= 'Z' or '0' <= expr[0] <= '9' or expr[0] == '_':
            identifier += expr[0]
            expr = expr[1:]
            continue
        break

    return expr, identifier


if __name__ == '__main__':
    main()
