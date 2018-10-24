import math
import qrcode
import sys
from PIL import Image, ImageDraw, ImageFont


class TextQRCode:
  def __init__(self):
    self.bgBlack="\033[40m"
    self.bgWhite="\033[47m"
    self.fgBlack="\033[0;30m"
    self.fgWhite="\033[0;37m"
    self.colorOff="\033[0m"
    self.colorMapping = {
      0: self.colorOff + " ",
      1: self.bgWhite + self.fgBlack + "▄",
      2: self.colorOff + "▄",
      3: self.colorOff + "█"
    }
    self.pixelAcceptance = 64

  def drawRow(self, row):
    line = ""
    for px in row:
      line += self.colorMapping[px]
    line += self.colorOff
    print(line)
    
  def draw(self, blocks):
    colors = []
    lenBlocks = len(blocks)
    if lenBlocks == 0:
      return colors
    cellLen = len(blocks[0])

    for i in range(math.ceil(len(blocks)/2)):
      colorRow, iterSize = [], 2
      if i*2+1>=lenBlocks:
        iterSize = 1
      for j in range(cellLen):
        for k in range(iterSize):
          px = blocks[i*2+k][j]*2**k
          if k == 0:
            colorRow.append(px)
          else:
            colorRow[j] += px
      self.drawRow(colorRow)
      colors.append(colorRow)
    return colors

  def draw_im(self, im):
    im = im.convert('RGB')
    res = []
    for y in range(int(im.size[1])):
      row = []
      for x in range(int(im.size[0])):
        p = im.getpixel((x,y))
        if p[0] < self.pixelAcceptance:
          row.append(0)
        else:
          row.append(1)
      res.append(row)
    self.draw(res)

  def draw_qrcode(self, text):
    qr = qrcode.QRCode(
      version=1,
      box_size=2,
      border=1
    )
    qr.add_data(text)
    qr.make(fit=True)
    im = qr.make_image(fill="black", back_color="white")
    whiteColor = (255, 255, 255)
    blackColor = (0,0,0)
    self.draw_im(im)
    del im

if __name__ == "__main__":
  if len(sys.argv) >1:
    argv = sys.argv[1:]
    line = " ".join(argv)
    t = TextQRCode()
    t.draw_qrcode(line)

