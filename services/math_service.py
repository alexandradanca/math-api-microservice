class MathService:
    @staticmethod
    def pow(base, exp):
        return base ** exp

    @staticmethod
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

    @staticmethod
    def factorial(n):
        if n < 0:
            raise ValueError("Negative numbers do not have factorials.")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
