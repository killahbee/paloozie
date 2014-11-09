import string
import random
import time

def id_generator(size=40, chars=string.ascii_lowercase + string.digits):
	return (str(hex( int(time.time()) * 1000 )[2:]) + '-' + ''.join(random.choice(chars) for _ in range(size)))[:42]