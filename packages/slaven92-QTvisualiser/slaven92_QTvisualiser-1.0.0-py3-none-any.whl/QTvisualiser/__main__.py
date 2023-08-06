import sys

from .app import App2

def main():
    app = App2([])
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()