from betterLogger import ClassWithLogger, push_name_to_logger_name_stack


class Lexer(ClassWithLogger):
    J_code: str
    file_path: str

    def __init__(self, J_code, file_path):
        ClassWithLogger.__init__(self)

        self.J_code = J_code
        self.file_path = file_path

        self.push_logger_name(f"\"{self.file_path}\"")

    @push_name_to_logger_name_stack
    def get_tokens(self):
        self.log_debug("Getting tokens for self")
        self.log_trace(f"Script is:\n{self.J_code}")
