import math
import cmath

class Heston:
    def __init__(
        self,
        spot,
        strike,
        maturity,
        risk_free_rate,
        dividend_yield,
        type,
        volatility,
        reversion_level,
        reversion_rate,
        vol_of_vol,
        correlation,
    ):
        self._s = float(spot)
        self._k = float(strike)
        self._mat = float(maturity)
        self._r = float(risk_free_rate)
        self._q = float(dividend_yield)
        self._type = type
        self._v0 = complex(volatility ** 2)
        self._kappa = float(reversion_rate)
        self._theta = float(reversion_level ** 2)
        self._xi = float(vol_of_vol)
        self._rho = float(correlation)
        self._x0 = 0 + 0j
        self._C = 0 + 0j
        self._dx = 0 + 0j
        self._Dv = 0 + 0j
        self._x = []
        self._w = []
        self._nInt = 0

    def get_price(self):
        n = 50
        self.gauss_laguerre(n)

        sp = 0.0
        sq = 0.0
        for i in range(n):
            sp += self.heston_cdf(self._x[i], 1) * self._w[i]
            sq += self.heston_cdf(self._x[i], 2) * self._w[i]

        PP = 0.5 + sp / math.pi
        QQ = 0.5 + sq / math.pi
        callprice = (
            self._s * math.exp(-self._q * self._mat) * PP
            - self._k * math.exp(-self._r * self._mat) * QQ
        )

        is_call = (
            isinstance(self._type, bool)
            and self._type
            or str(self._type).strip().lower() == "call"
        )

        if is_call:
            return callprice
        return callprice - (
            self._s * math.exp(-self._q * self._mat)
            - self._k * math.exp(-self._r * self._mat)
        )

    def calc_phi(self, alpha, beta):
        self.calc_cd(alpha, beta)
        return cmath.exp(self._C + self._dx * self._x0 + self._Dv * self._v0)

    def heston_cdf(self, omega, n):
        log_k = math.log(self._k / self._s) - (self._r - self._q) * self._mat

        if n == 1:
            phi = self.calc_phi(complex(omega, -1), complex(0, 0))
            return (cmath.exp(complex(0, -omega * log_k)) * phi / complex(0, omega)).real
        if n == 2:
            phi = self.calc_phi(complex(omega, 0), complex(0, 0))
            return (cmath.exp(complex(0, -omega * log_k)) * phi / complex(0, omega)).real
        return 0.0

    def gauss_laguerre(self, n):
        if self._nInt == n:
            return
        self._nInt = n
        self._x = [0.0] * n
        self._w = [0.0] * n

        for i in range(n):
            if i == 0:
                z = 3.0 / (1.0 + 2.4 * n)
            elif i == 1:
                z += 15.0 / (1.0 + 2.5 * n)
            else:
                h = i - 1
                z += ((1.0 + 2.55 * h) / (1.9 * h)) * (z - self._x[i - 2])

            while True:
                p0 = 1.0
                p1 = 1.0 - z
                for j in range(1, n):
                    p2 = ((2.0 * j + 1.0 - z) * p1 - j * p0) / (j + 1.0)
                    if j < n - 1:
                        p0 = p1
                        p1 = p2
                deri = (n * p2 - n * p1) / z
                step = p2 / deri
                z -= step
                if abs(step) < 1.001e-15 * n:
                    break

            self._x[i] = z
            self._w[i] = -1.0 / (deri * n * p1)
            self._w[i] *= math.exp(z)

    def calc_cd(self, alpha, beta):
        xi2 = self._xi * self._xi
        m = complex(self._kappa, 0) - alpha * complex(0, self._rho * self._xi)
        d = cmath.sqrt(complex(xi2, 0) * alpha * (alpha + complex(0, 1)) + m * m)
        mmd = m - d
        mpd = m + d
        g = mmd / mpd
        delta = beta * complex(0, 1)
        xd = complex(xi2, 0) * delta
        gh = (mmd - xd) / (mpd - xd)
        edt = cmath.exp(-d * self._mat)
        ghe = gh * edt
        c1 = mmd * complex(self._kappa * self._theta * self._mat / xi2, 0)
        c2 = (complex(1, 0) - gh) / (complex(1, 0) - ghe)
        c2 = cmath.log(c2) * complex(2.0 * self._kappa * self._theta / xi2, 0)
        self._C = c1 + c2
        self._dx = complex(0, 1) * alpha
        self._Dv = mpd / complex(xi2, 0) * ((g - ghe) / (complex(1, 0) - ghe))