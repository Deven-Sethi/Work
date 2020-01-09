import unittest
import MainNew
from math import sqrt, exp, log, pi

class TestMainNew(unittest.TestCase):
	def test_coefficients(self):
		#Note that the coefficients for BlackScholes and BAchelier are independent of: ID, OptionType, Market Price
		trade = MainNew.BlackScholes(1, 'Stock', 113.5, 0.008, 152.08333333, 115.0, 'Call', 'BlackScholes', 1)
		self.assertAlmostEqual(trade.coefficients(0.12)[0], -0.08774, places=4)
		self.assertAlmostEqual(trade.coefficients(0.12)[1], -0.1652, places=4)

		trade = MainNew.BlackScholes(1, 'Stock', 50.0, 0.02, 80.0, 45.0, 'Call', 'BlackScholes', 1)
		self.assertAlmostEqual(trade.coefficients(0.3)[0], 0.851, places=2)
		self.assertAlmostEqual(trade.coefficients(0.3)[1], 0.711, places=2)

	def test_callPrice(self):
		trade = MainNew.BlackScholes(1, 'Stock', 50.0, 0.02, 80.0, 45.0, 'Call', 'BlackScholes', 1)
		d1, d2 = trade.coefficients(0.3)
		C = trade.callPrice(0.3, d1, d2)
		self.assertAlmostEqual(C, 6.02, places=2)

		trade = MainNew.BlackScholes(1, 'Stock', 1.5820, -0.0017, 147.1770, 1.8987, 'Call', 'BlackScholes', 1)
		d1, d2 = trade.coefficients(1.81853888892)
		C = trade.callPrice(1.81853888892, d1, d2)
		self.assertAlmostEqual(C, 0.60912744, places=2)

		trade = MainNew.BlackScholes(1, 'Future', 0.48254625363791304*exp(0.0019*0.8145728767123287), -0.0019, 0.8145728767123287*365.0, 0.6190, 'Call', 'BlackScholes', 1)
		d1, d2 = trade.coefficients(1.7565512677766049)
		C = trade.callPrice(1.7565512677766049, d1, d2)
		self.assertAlmostEqual(C, 0.24978226, places = 2)

		trade = MainNew.Bachelier(1,'Future',0.8731,-0.0025,278.2703,1.0610,'Call','Bachelier',0.40362827)
		d1 = trade.coefficient(1.4098504789475481)
		C = trade.callPrice(1.4098504789475481, d1)
		self.assertAlmostEqual(C, 0.40362827, places = 2)

	def test_putPrice(self):
		trade = MainNew.BlackScholes(1, 'Stock', 113.5, 0.008, 152.08333333, 115.0, 'Call', 'BlackScholes', 1)
		d1, d2 = trade.coefficients(0.12)
		P = trade.putPrice(0.12, d1, d2)
		self.assertAlmostEqual(P, 4.108711, places=1)

		trade = MainNew.BlackScholes(1, 'Stock', 42.0, 0.10, 0.5*365.0, 40, 'Put', 'BlackScholes', 1)
		d1, d2 = trade.coefficients(0.2)
		P = trade.putPrice(0.2, d1, d2)
		self.assertAlmostEqual(P, 0.81, places=2)

		trade = MainNew.Bachelier(0,'Future',1.9119,-0.0009,19.3599,2.0264,'Call','Bachelier',0.096576518)
		d1 = trade.coefficient(1.5974363602445016)
		P = trade.callPrice(1.5974363602445016, d1)
		self.assertAlmostEqual(P, 0.096576518, places = 2)

	def test_impliedVolatility(self):
		trade = MainNew.BlackScholes(1, 'Stock', 10.0, 0.04, 365.0, 10.0, 'Call', 'BlackScholes', 1.38)
		self.assertAlmostEqual(trade.impliedVolatility(), 0.3, places = 2)

		trade = MainNew.BlackScholes(1, 'Stock', 42.0, 0.10, 365.0/2.0, 40, 'Call', 'BlackScholes', 4.76)
		self.assertAlmostEqual(trade.impliedVolatility(), 0.2, places = 1)

		trade = MainNew.BlackScholes(1, 'Stock', 20*exp(-0.09*4.0/12.0), 0.09, 4.0*365.0/12.0, 20, 'Put', 'BlackScholes', 1.12)
		self.assertAlmostEqual(trade.impliedVolatility(), 0.25, places = 2)

		trade = MainNew.Bachelier(63,'Future',0.7015,-0.0035,58.5400,0.7248,'Call','Bachelier',0.071237347)
		self.assertAlmostEqual(trade.impliedVolatility(), 0.5152674904324781, places = 7)

		trade = MainNew.Bachelier(64,'Stock',1.7523,-0.0047,19.4579,1.8251,'Put','Bachelier',0.14361378)
		self.assertAlmostEqual(trade.impliedVolatility(), 2.029726696912237, places = 7)







#ID,Underlying Type,Underlying,Risk-Free Rate,Days To Expiry,Strike,Option Type,
#Model Type,Market Price
#0,Future,1.9119,-0.0009,19.3599,2.0264,Call,Bachelier,0.096576518


if __name__=='__main__':
	unittest.main()


