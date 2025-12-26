"""
Natural Language to Python Code Generator
Author: Komal Mandal

Description:
This program converts simple natural language instructions
into valid Python code using a rule-based NLP approach.
"""

class CodeGenerator:

    def __init__(self, instruction: str):
        self.instruction = instruction.lower()

    def extract_numbers(self):
        """Extract numeric values from instruction"""
        return [int(word) for word in self.instruction.split() if word.isdigit()]

    def generate_code(self):
        """Generate Python code based on detected intent"""

        # Rule 1: Print numbers in a range
        if "print numbers" in self.instruction:
            nums = self.extract_numbers()
            if len(nums) == 2:
                return self.print_numbers(nums[0], nums[1])

        # Rule 2: Print text
        if self.instruction.startswith("print"):
            return self.print_text()

        # Rule 3: Add two numbers
        if "add" in self.instruction:
            nums = self.extract_numbers()
            if len(nums) == 2:
                return self.add_numbers(nums[0], nums[1])

        return "# Unable to understand the instruction"

    def print_numbers(self, start, end):
        return f"""for i in range({start}, {end + 1}):
    print(i)"""

    def print_text(self):
        text = self.instruction.replace("print", "").strip()
        return f'print("{text}")'

    def add_numbers(self, a, b):
        return f"""result = {a} + {b}
print(result)"""


if __name__ == "__main__":
    user_input = input("Enter instruction: ")
    generator = CodeGenerator(user_input)
    code = generator.generate_code()

    print("\nGenerated Python Code:\n")
    print(code)
