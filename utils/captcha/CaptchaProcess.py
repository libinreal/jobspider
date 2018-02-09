# -*- coding: UTF-8 -*-

from BaseObject import BaseObject
import pytesseract
from PIL import Image
import os
import sys
import cv2
	

reload(sys)                         
sys.setdefaultencoding('utf-8')     

class CaptchaProcess(BaseObject):
	def __init__(self, indir='', outdir='', testdir=''):
		self.indir = indir
		self.outdir = outdir
		self.testdir = testdir
		self.total = 0
		self.correct = 0

	def tif(self):
		'''
		change format from .* to .tif
		'''
		dirs = os.listdir(self.indir)
		for f in dirs:
			sn = f.split('.')
			s = Image.open(self.indir + f)

			print ' save as tif : %s.tif' % sn[0]
			s.save(r"%s%s.tif" % (self.outdir, sn[0]) )

	def gray(self):
		'''
		change bpp(bits per pixel ) from N(N>8) to 8
		'''
		dirs = os.listdir(self.outdir)
		for f in dirs:
			sn = f.split('.')
			if len(sn) == 2 and sn[0].isdigit and sn[1] == 'tif':
				print 'save as 8 bpp : %s.tif' % sn[0]
				grayImage = cv2.imread(self.outdir + f, cv2.IMREAD_GRAYSCALE)
				cv2.imwrite(r"%s%s.tif" % (self.outdir, sn[0]), grayImage)

	def ocr(self):
		dirs = os.listdir(self.testdir)
		for f in dirs:
			sn = f.split('.')
			if len(sn) == 2 and sn[1] == 'tif':
				self.total += 1
				print '\n start identify %s.tif' % sn[0]
				captcha = Image.open(self.testdir + f)
				captchaCode = pytesseract.image_to_string(captcha)
				# captchaCode = captchaCode.decode('gbk').encode('utf-8')

				# sn[0] = sn[0].decode('gbk').encode('utf-8')
				print ' debug captcha: %s, debug file name: %s' %( self.encoding(captchaCode), self.encoding(sn[0]) )
				if captchaCode.upper() == sn[0][:4].upper():
					self.correct += 1

				print ' %s -> %s' % (sn[0][:4].upper().encode('GBK','ignore'), captchaCode.upper().encode('GBK','ignore'))
				print ' correct numbers:%s \n' % self.correct
		prec = (self.correct / float(self.total)) * 100
		print ' The precision of this whole ocr is %3.2f%% : (%d/%d) * 100%%' % ( prec, self.correct, self.total )

if __name__ == '__main__':
    sc = CaptchaProcess(r'd:/storage/captcha_ex/', r'd:/storage/captcha_ocr/', r'd:/storage/captcha_test/')
    sc.ocr()