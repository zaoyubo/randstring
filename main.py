import pytesseract
from PIL import Image,ImageEnhance

class img(object):
    def __init__(self, path, out_path):
        """
        :param path: 文件路径，directory 和 图片文件必须存在
        :param out_path: 输出路径，其中的 directory 必须存在，最后的 filename 可以不存在
        """
        self.img = self._openimg(path)
        self.out_path = out_path

    def _openimg(self, name):
        try:
            im = Image.open(name)
            return im
        except:
            print('[!] Open %s failed' % name)
            exit()

    def binarization(self):
        """
        二值化
        """
        threshold = 140 # 二值化阀值，可以调整
        table = []
        for i in range(256): # 构建二值化要用的 table
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        self.img = self.img.point(table, '1')

    def grey(self):
        """
        灰度化
        """
        self.img = self.img.convert('L')

    #能去除比验证码细很多的噪点和线
    def pIx(self):
        w,h =self.img.size
        for x in range(w):
            for y in range(h):
                sum = 0
                top = (x,y+1)
                bottom = (x,y-1)
                left = (x-1,y)
                lefttop = (x-1,y+1)
                leftbottom = (x-1,y-1)
                right = (x+1,y)
                righttop = (x+1,y+1)
                rightbottom = (x+1,y-1)

                pixel = self.img.getpixel((x,y))
                if pixel == 0:
                    if x>0:
                        # 左
                        p = self.img.getpixel(left)
                        if p == 0:
                            sum = sum + 1
                    if x<w-1:
                        # 右
                        p = self.img.getpixel(right)
                        if p == 0:
                            sum = sum + 1
                    if y>0:
                        # 下
                        p = self.img.getpixel(bottom)
                        if p == 0:
                            sum = sum + 1
                    if y<h-1:
                        # 上
                        p = self.img.getpixel(top)
                        if p == 0:
                            sum = sum + 1
                    if x!=0 and y!=h-1:
                        #左上
                        p = self.img.getpixel(lefttop)
                        if p == 0:
                            sum = sum + 1
                    if x!=w-1 and y!=0:
                        #右下
                        p = self.img.getpixel(rightbottom)
                        if p == 0:
                            sum = sum + 1
                    if x!=w-1 and y!=h-1:
                        #右上
                        p = self.img.getpixel(righttop)
                        if p == 0:
                            sum = sum + 1
                    if x!=0 and y!=0:
                        #左下
                        p = self.img.getpixel(leftbottom)
                        if p == 0:
                            sum = sum + 1
                    if sum < 4:
                        self.img.putpixel((x,y),255)


    def process(self):
        self.grey()
        self.binarization()
        self.pIx()
        self.img.save(self.out_path)

    def result(self):
        """
        将易错的字符手动替换一下，返回最终结果
        :return:
        """
        rep = {'0': 'O',
               '1': 'I',
               '2': 'Z',
               '8': 'B',
               # 'O': 'Q',
               '6': 'E',
               ' ': '',
               # 'V': 'Y'
               }
        text = pytesseract.image_to_string(self.img)
        for r in rep:
            text = text.replace(r, rep[r])
        return text.strip("")


if __name__ == '__main__':
    img = img("./randstring_jpgs/10.jpg","./processed_jpgs/10.jpg")
    img.process()
    print(img.result())

