import pytest
from pylumenta.generator import jedanPolumenta, Polumente, rodiPolumentu

def test_jedanPolumenta():	
	pol = jedanPolumenta()
	assert(pol != '')
	assert(len(pol) > 3)
	assert(len(pol.split()) == 1)


def test_Polumente_low():
	poli = Polumente(-20)
	assert(len(poli) == 1)

def test_Polumente_high():
	with pytest.raises(ValueError):
		poli = Polumente(200)

def test_Polumente_num():
	poli = Polumente(20)
	assert(len(poli) == 20)
