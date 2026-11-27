import sys

from src import App

if __name__ == '__main__':

    try:
        if len(sys.argv) != 2:
            raise ValueError(
                """Incorrect number of arguments provided.
Correct call:
python pac-man.py <config file>
""")
        path = sys.argv[1]
        app = App(path, (700, 600))
        app.launch()
    except Exception as e:
        print(f"The application encountered an error: {str(e)}")
