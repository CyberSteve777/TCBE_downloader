from utils import clone
import os


if __name__ == '__main__':
    print("Downloading to:", os.getcwd())
    clone("https://github.com/Ryorama/TerrariaCraft-Bedrock")
    print("\nSuccessfully downloaded")
