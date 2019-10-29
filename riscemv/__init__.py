import sys
name = "riscemv"

def main_gui():
    from riscemv.gui.main import launch
    launch()


if __name__ == "__main__":
    # Running as standalone program
    main_gui()
