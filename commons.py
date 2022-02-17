import datetime

def get_now():
    return datetime.datetime.now().time()

class LangParams:
    def __init__(self, cmd, skip: list = []) -> None:
        self.command = cmd
        self.interations_to_skip = skip

languages = {
    "c":        LangParams(".\\c-logistic-benchmark\\x64\\Debug\\c-logistic-benchmark.exe"),
    "c#":       LangParams(".\\cs-logistic-beanchmark\\bin\\Debug\\net6.0\\cs-logistic-beanchmark.exe"),
    "go":       LangParams(".\\go-logistic-benchmark\\go-logistic-benchmark.exe"),
    "java":     LangParams("java -jar .\\java-logistic-benchmark\\logistic-benchmark\\target\\java-logistic-benchmark-jar-with-dependencies.jar"),
    "node":     LangParams("npm start --prefix typescript-logistic-benchmark --"),
    "python":   LangParams("python .\\python-logistic-benchmark\\main.py"),
}


