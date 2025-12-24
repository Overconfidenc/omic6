from entities import IView

class ConsoleView(IView):
    def display(self, data):
        print(f"[INFO] {data}")
    
    def update(self, data):
        print(f"\n >>> [STATUS UPDATE] {data} <<<\n")