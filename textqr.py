import math
import qrcode
import sys
from PIL import Image, ImageDraw, ImageFont


class TextQRCode:
  def __init__(self):
    self.colorOff="\033[0m"
    self.colorMapping = {
      0: "\033[0m" + " ",
      1: "\033[30;47m" + "▄",
      2: "\033[0m" + "▄",
      3: "\033[0m" + "█"
    }
    self.pixelAcceptance = 64

    self.qr = qrcode.QRCode(
      version=1,
      box_size=1,
      border=1
    )

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
    self.qr.add_data(text)
    self.qr.make(fit=True)
    im = self.qr.make_image(fill="black", back_color="white")
    whiteColor = (255, 255, 255)
    blackColor = (0,0,0)
    # im = im.resize((im.size[0]//2, im.size[1]//2), Image.BICUBIC)
    self.draw_im(im)
    del im

  def _banner_ch(self, text):
    whiteColor = (255, 255, 255)
    blackColor = (0,0,0)
    size = 9
    im = Image.new ("RGB", (size, int(size*1.5)), whiteColor)
    draw = ImageDraw.Draw(im)
    draw.text((0,0), text, fill=blackColor)
    res = ""
    for y in range(int(size*1.5)):
      for x in range(size):
        p = im.getpixel((x,y))
        if p[0] ==0:
          res += "#"
        else:
          res += " "
      res += "\n"
    del im
    return res

  def banner(self, text):
    chars = []
    for i in range(len(text)):
      ch = self._banner_ch(text[i])
      lines = ch.split("\n")
      if len(chars) ==0:
        chars.extend(lines)
      else:
        for j in range(len(lines)):
          chars[j]+= lines[j]

    res = []
    for j in range(len(chars)):
      row = []
      for k in chars[j]:
        if k == "#":
          row.append(1)
        else:
          row.append(0)
      if len(row)>0:
        res.append(row)
    self.draw(res)

if __name__ == "__main__":
  if len(sys.argv) >1:
    argv = sys.argv[1:]
    line = " ".join(argv)
    t = TextQRCode()
    # t.banner(line)
    t.draw_qrcode(line)

