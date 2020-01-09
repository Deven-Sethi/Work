import csv
from math import sqrt, exp, log, pi
from scipy.stats import norm

class Trade:
	def __init__(self, ID, UnderlyingType, Underlying, RiskFreeRate, DaysToExpiry, Strike, OptionType, ModelType, MarketPrice):
		self.ID = ID
		self.UnderlyingType = UnderlyingType
		self.Underlying = float(Underlying)
		self.r = float(RiskFreeRate)
		self.t = float(DaysToExpiry)/365.0
		self.K = float(Strike)
		self.OptionType = OptionType
		self.ModelType = ModelType
		self.MarketPrice = float(MarketPrice)
		if self.UnderlyingType == "Stock": 
			self.Spot = self.Underlying 
		else: 
			self.Spot = self.Underlying*exp(-self.r *self.t)
		pass

	#returns the time in years
	def time(self):
		return(self.t)

	def spot(self):
		return(self.Spot)

class BlackScholes(Trade):
	def __init__(self, ID, UnderlyingType, Underlying, RiskFreeRate, DaysToExpiry, Strike, OptionType, ModelType, MarketPrice):
		super().__init__(ID, UnderlyingType, Underlying, RiskFreeRate, DaysToExpiry, Strike, OptionType, ModelType, MarketPrice)

	def coefficients(self, sigma):
		d1 = 1 / (sigma * sqrt(self.t)) * (log(self.Spot / self.K) + (self.r + (sigma**2)/2) * self.t )
		d2 = d1 - sigma * sqrt(self.t)
		return(d1, d2)

	def callPrice(self, sigma, d1,d2):
		C = norm.cdf(d1) * self.Spot - norm.cdf(d2) * self.K * exp(-self.r * self.t)
		return(C)

	def putPrice(self, sigma, d1, d2): 
		P = norm.cdf(-d2) * self.K * exp(-self.r * self.t) - norm.cdf(-d1) * self.Spot 
		return(P)

	def vega(self, d1):
		vega = self.Spot * norm.pdf(d1)*sqrt(self.t)
		return(vega)
	
	def coefficients(self, sigma):
		d1 = 1 / (sigma * sqrt(self.t)) * (log(self.Spot / self.K) + (self.r + (sigma**2)/2) * self.t )
		d2 = d1 - sigma * sqrt(self.t)
		return(d1, d2)

	def function(self, vol, d1, d2):
		if self.OptionType =='Call': 
			function = self.callPrice(vol, d1, d2) - self.MarketPrice
		else: 
			function = self.putPrice(vol, d1, d2) - self.MarketPrice
		return(function)

	def impliedVolatility(self):
		#Tolerence 
		tol, delta = 1*10**(-8), 1

		Index, MaxIndex = 0, 1000

		vol = 0.5

		while delta>tol:

			Index = Index + 1
			if Index>=MaxIndex:
				print("NAN")
				return;

			original_vol = vol

			d1, d2 = self.coefficients(vol)
			function = self.function(vol, d1, d2) 
			vega = self.vega(d1)

			if vega == 0:
				return("NAN")

			#this is an application of the newton raphson method applied to the equations CallPrice - C0 = 0 and PutPrice - P0 = 0
			vol = vol - function/vega

			delta = abs((vol - original_vol)/original_vol)

		return(vol)

class Bachelier(Trade):
	def __init__(self, ID, UnderlyingType, Underlying, RiskFreeRate, DaysToExpiry, Strike, OptionType, ModelType, MarketPrice):
		super().__init__(ID, UnderlyingType, Underlying, RiskFreeRate, DaysToExpiry, Strike, OptionType, ModelType, MarketPrice)

	def coefficient(self, vol):
		d1 = (self.Spot - self.K) / (vol * sqrt(self.t))
		return(d1)

	def callPrice(self, vol, d1):
		#decide if this formulae should be P = e^(-rt)( vol * sqrt(t) * norm.pdf(d1) + (S - K)*norm.cdf(d1))
		P = exp(-self.r * self.t) * vol * sqrt(self.t) * norm.pdf(d1) + (self.Spot - self.K * exp(-self.r * self.t))*norm.cdf(d1)
		return(P)

	def putPrice(self, vol, d1):
		#decide if this formulae should be P = e^(-rt)( vol * sqrt(t) * norm.pdf(d1) + (S - K)*norm.cdf(d1))
		P = exp(-self.r * self.t) * vol * sqrt(self.t) * norm.pdf(d1) + (self.Spot - self.K * exp(-self.r * self.t))*norm.cdf(-d1)
		return(P)

	def vega(self, d1):
		vega = exp(-self.r * self.t) * norm.pdf(d1)*sqrt(self.t)
		return(vega)

	def coefficient(self, vol):
		d1 = (self.Spot - self.K) / (vol * sqrt(self.t))
		return(d1)

	def function(self, vol, d1):
		if self.OptionType =='Call': 
			function = self.callPrice(vol, d1) - self.MarketPrice
		else: 
			function = self.putPrice(vol, d1) - self.MarketPrice
		return(function)

	def impliedVolatility(self):
		if self.Spot == self.K:
			#This is when an option is at the money
			#Call Price = e^(-rt)(sigma sqrt(t)/ sqrt(2pi)
			#Put Price = e^(-rt)(sigma sqrt(t)/ sqrt(2pi))
			sigma = sqrt(2 * pi / self.t) * self.MarketPrice * exp(self.r * self.t) 
			return(sigma)

		#Tolerence 
		tol, delta = 1*10**(-8), 1

		Index, MaxIndex = 0, 1000

		#This is an initial input so the difference equation is well defined
		vol = 5

		while delta>tol:

			Index = Index + 1
			if Index>=MaxIndex:
				print("NAN")
				return;

			original_vol = vol

			d1 = self.coefficient(vol)
			function = self.function(vol, d1) 
			vega = self.vega(d1)

			if vega == 0:
				return("NAN")

			#this is an application of the newton raphson method applied to the equations CallPrice - C0 = 0 and PutPrice - P0 = 0
			vol = vol - function/vega

			delta = abs((vol - original_vol)/original_vol)

		return(vol)

def main():
	with open('input.csv','r') as csv_file:
		csv_reader = csv.reader(csv_file)

		with open('output.csv', 'w') as new_file:

			fieldnames = ['ID', 'Spot', 'Strike', 'Risk-Free Rate', 
						'Years To Expiry', 'Option Type', 'Model Type', 
						'Implied Volatility', 'Market Price']

			csv_writer = csv.DictWriter(new_file, fieldnames = fieldnames, delimiter=',')

			next(csv_reader)

			csv_writer.writeheader()

			for line in csv_reader:

				trade = None
				if line[7] == 'BlackScholes':
					trade = BlackScholes(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8])
				else:
					trade = Bachelier(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8])

				Spot = trade.spot()
				Time = trade.time()

				csv_writer.writerow({'ID' : line[0],
									'Spot': Spot,
									'Strike': line[5],
									'Risk-Free Rate' : line[3],
									'Years To Expiry' : Time,
									'Option Type' : line[6],
									'Model Type' : line[7],
									'Implied Volatility' : trade.impliedVolatility(),   
									'Market Price' : line[8]})
	pass

main()